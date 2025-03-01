import base64
import re
from contextlib import contextmanager
from typing import Dict, List
from tempfile import NamedTemporaryFile

from kubernetes.client import ApiException
from yaml import safe_dump
from boto3.session import Session


def get_cluster_info(instance_name: str, repo_name: str, session: Session):
    client = session.client("eks")
    clusters = client.list_clusters()["clusters"]
    for cluster in clusters:
        cluster_info = client.describe_cluster(name=cluster)["cluster"]
        tag_instance_name = cluster_info["tags"].get("instance_name")
        tag_repo_name = cluster_info["tags"].get("repo_name")

        if (
            tag_repo_name
            and tag_repo_name == repo_name
            and tag_instance_name
            and tag_instance_name == instance_name
        ):
            return cluster_info

    raise Exception(
        f"No cluster found for instance_name: {instance_name}, repo_name: {repo_name}"
    )


def get_cluster_token(session: Session):
    url = session.client("sts").generate_presigned_url(
        "get_caller_identity", Params={}, ExpiresIn=60, HttpMethod="GET"
    )
    token = "k8s-aws-v1." + base64.urlsafe_b64encode(url.encode("utf-8")).decode(
        "utf-8"
    ).rstrip("=")
    return token


@contextmanager
def create_kubeconfig(
    instance_name: str,
    session: Session,
    profile: str,
    aws_region: str,
    repo_name: str = "hmd-inf-eks",
    assume_role: bool = False,
):
    """Create a temporary kubeconfig file that can be used in k8s operations.

    A context manager that creates a temporary kubeconfig file and returns the file name
    for use. When the context manager is complete, the file is deleted. This is useful
    for issuing helm commands or using the kubernetes python API.

    Usage::
        with create_kubeconfig(instance_name, session, profile, region, repo_name, context_name) as kubeconfig:
            # do the work
            # ...

    :param instance_name: The eks cluster instance name.
    :param session: A session that has access to retrieve cluster information.
    :param profile: A profile name (can be None) that will be added to the user config.
    :param region: The AWS region in which the cluster is located.
    :param repo_name: The repo_name of the eks repo class.
    :return:
    """
    context_name = "the_context"
    cluster_info = get_cluster_info(instance_name, repo_name, session)
    account_number = session.client("sts").get_caller_identity().get("Account")

    exec_command = {
        "apiVersion": "client.authentication.k8s.io/v1beta1",
        "command": "aws",
        "args": [
            "eks",
            "--region",
            aws_region,
            "get-token",
            "--cluster-name",
            cluster_info["name"],
        ],
    }

    if profile:
        exec_command["env"] = [{"name": "AWS_PROFILE", "value": profile}]
    if assume_role:
        exec_command["args"] += [
            "--role",
            f"arn:aws:iam::{account_number}:role/hmd.neuronsphere.deploy",
        ]

    kubeconfig = {
        "current-context": context_name,
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [
            {
                "cluster": {
                    "certificate-authority-data": cluster_info["certificateAuthority"][
                        "data"
                    ],
                    "server": cluster_info["endpoint"],
                },
                "name": "the_cluster",
            }
        ],
        "contexts": [
            {
                "context": {
                    "cluster": "the_cluster",
                    "namespace": instance_name,
                    "user": "the_user",
                },
                "name": context_name,
            }
        ],
        "users": [{"name": "the_user", "user": {"exec": exec_command}}],
    }

    try:
        with NamedTemporaryFile("w") as temp_file:
            safe_dump(kubeconfig, temp_file)
            yield temp_file.name
    finally:
        pass


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def get_methods(k8s_client, kind):
    namespaced = True
    if hasattr(k8s_client, f"read_namespaced_{kind}"):
        read_method = getattr(k8s_client, f"read_namespaced_{kind}")
        create_method = getattr(k8s_client, f"create_namespaced_{kind}")
        patch_method = getattr(k8s_client, f"patch_namespaced_{kind}")

    elif hasattr(k8s_client, f"read_{kind}"):
        read_method = getattr(k8s_client, f"read_{kind}")
        create_method = getattr(k8s_client, f"create_{kind}")
        patch_method = getattr(k8s_client, f"patch_{kind}")
        namespaced = False

    else:
        raise Exception(f"No methods found on k8s client for kind, {kind}")

    return namespaced, read_method, create_method, patch_method


def apply_k8s_manifests(k8s_client, data: List):
    for manifest in data:
        group, _, version = manifest["apiVersion"].partition("/")
        if version == "":
            version = group
            group = "core"
        # Take care for the case e.g. api_type is "apiextensions.k8s.io"
        # Only replace the last instance
        group = "".join(group.rsplit(".k8s.io", 1))
        # convert group name from DNS subdomain format to
        # python class name convention
        group = "".join(word.capitalize() for word in group.split("."))
        fcn_to_call = "{0}{1}Api".format(group, version.capitalize())
        k8s_api = getattr(k8s_client, fcn_to_call)()

        kind = camel_to_snake(manifest["kind"])
        namespace = manifest["metadata"].get("namespace")
        namespaced, read_method, create_method, patch_method = get_methods(
            k8s_api, kind
        )
        try:
            kwargs = {} if not namespaced else {"namespace": namespace}
            read_method(manifest["metadata"]["name"], **kwargs)
        except ApiException as apiex:
            if apiex.status == 404:
                create_method(body=manifest, **kwargs)
            else:
                raise apiex
        else:
            patch_method(manifest["metadata"]["name"], body=manifest, **kwargs)
