from hmd_cli_tools.hmd_cli_tools import cd, create_secret, gen_password, format_tags
from boto3 import Session
from cement.utils import shell
from shutil import rmtree
from typing import Dict
import re


def generate_vpn_config(
    session: Session, client_vpn_endpoint_id: str, client_cidr: str
) -> str:
    ec2 = session.client("ec2")
    sm = session.client("secretsmanager")
    config = ec2.export_client_vpn_client_configuration(
        ClientVpnEndpointId=client_vpn_endpoint_id
    ).get("ClientConfiguration", "")

    config = config.replace(
        f"{client_vpn_endpoint_id}.",
        f"{gen_password(length=5, include_symbols=False)}.{client_vpn_endpoint_id}.",
    )

    for secret_type in ["certificate", "key"]:
        secret = sm.get_secret_value(SecretId=f"client-vpn-client-{secret_type}").get(
            "SecretString", ""
        )
        config = config.replace("</ca>", f"</ca>\n{secret}")

    # adds route to enable internet connection while connected
    client_ip = client_cidr.split(".")[0] + "." + client_cidr.split(".")[1] + ".0.0"
    config = config.replace(
        "nobind", f"nobind\nroute-nopull\nroute {client_ip} 255.255.0.0"
    )

    config_file_path = f"./{client_vpn_endpoint_id}.ovpn"
    with open(config_file_path, "w") as f:
        f.write(config)

    return config_file_path


def put_vpn_certificates(
    session: Session,
    domain: str = None,
    renewal: bool = False,
    client_certificate: str = None,
    client_key: str = None,
    server_certificate: str = None,
    server_key: str = None,
    tags: Dict = {"ad-hoc": gen_password(include_symbols=False)},
) -> str:
    try:
        domain = domain or "hmdlabs.io"  # TODO: add correct naming

        if client_certificate or client_key or server_certificate or server_key:
            if (
                not client_certificate
                and client_key
                and server_certificate
                and server_key
            ):
                raise Exception(
                    "Client Key, Client Cert, Server Key, and Server Cert must all be provided."
                )

            _import_acm_certificate(
                session,
                f"server.{domain}",
                renewal,
                server_certificate,
                server_key,
                tags,
            )
            _import_acm_certificate(
                session,
                f"client.{domain}",
                renewal,
                client_certificate,
                client_key,
                tags,
            )
        else:
            _generate_and_import_certificates(session, domain, renewal, tags)

        return "VPN certificates are bootstrapped"
    except Exception as e:
        raise e


def _generate_and_import_certificates(
    session: Session, domain: str, renewal: bool, tags: Dict
):
    try:
        shell.exec_cmd2(
            "git clone -b v3.0.8 https://github.com/OpenVPN/easy-rsa.git".split()
        )

        easy_rsa_bin = "./easyrsa"
        certificate_commands = [
            [easy_rsa_bin, "init-pki"],
            ["sh", "-c", f"echo 'hmdlabs.io' | {easy_rsa_bin} build-ca nopass"],
            [easy_rsa_bin, "build-server-full", f"server.{domain}", "nopass"],
            [easy_rsa_bin, "build-client-full", f"client.{domain}", "nopass"],
        ]

        with cd("easy-rsa/easyrsa3"):
            for command in certificate_commands:
                shell.exec_cmd2(command)

            for certificate_type in ["server", "client"]:
                fqdn = f"{certificate_type}.{domain}"
                _import_acm_certificate(
                    session,
                    fqdn,
                    renewal,
                    f"pki/issued/{fqdn}.crt",
                    f"pki/private/{fqdn}.key",
                    tags,
                )
    except Exception as e:
        raise e
    finally:
        rmtree("easy-rsa")


def _import_acm_certificate(
    session: Session,
    fqdn: str,
    renewal: bool,
    certificate_path: str,
    key_path: str,
    tags: Dict,
):
    existing_cert = get_acm_certificate(session, fqdn)

    if renewal or not existing_cert:
        certificate_args = {
            "Certificate": open(certificate_path, "rb").read(),
            "PrivateKey": open(key_path, "rb").read(),
            "CertificateChain": open("pki/ca.crt", "rb").read(),
        }

        if existing_cert:
            certificate_args["CertificateArn"] = existing_cert.get("CertificateArn", "")
        else:
            certificate_args["Tags"] = format_tags(tags)

        response = session.client("acm").import_certificate(**certificate_args)

        if "client." in fqdn:
            _generate_vpn_certificate_secrets(
                session,
                open(certificate_path, "r").read(),
                open(key_path, "r").read(),
                tags,
            )


def _generate_vpn_certificate_secrets(
    session: Session, certificate: bytes, key: bytes, tags: list
):
    key = f"<key>\n{key}</key>"
    cert = re.findall("-----BEGIN .+?-----(?s).+?-----END .+?-----", certificate)
    cert = f"<cert>\n{cert[-1]}\n</cert>"

    # TODO: Use correct naming on secret names
    create_secret(
        session, "client-vpn-client-certificate", cert, tags=tags, exists_ok=True
    )
    create_secret(session, "client-vpn-client-key", key, tags=tags, exists_ok=True)


def get_acm_certificate(session: Session, fqdn: str) -> Dict:
    return next(
        iter(
            [
                c
                for c in _list_acm_certificates(session)
                if fqdn == c.get("DomainName", "")
            ]
        ),
        {},
    )


def _list_acm_certificates(session: Session) -> list:
    existing_certificates = []

    paginator = session.client("acm").get_paginator("list_certificates")
    for certificates in paginator.paginate():
        existing_certificates = existing_certificates + certificates.get(
            "CertificateSummaryList", []
        )

    return existing_certificates
