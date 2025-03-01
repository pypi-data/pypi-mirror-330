import argparse
import collections.abc
import json
import os
import secrets
from contextlib import contextmanager
from functools import wraps
from json import JSONDecodeError, dumps, loads
from pathlib import Path
from random import shuffle
from time import sleep
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Union

import requests
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig
from boto3 import Session
from cement.ext.ext_argparse import ArgparseArgumentHandler
from dotenv import load_dotenv, set_key

TOOL_PROFILE = "hmd_tool_profile"


def get_session(aws_region: str = None, profile: str = None) -> Session:
    """Create an AWS ``Session`` object.

    :param aws_region: the AWS region name, defaults to None
    :type aws_region: str, optional
    :param profile: the AWS profile, defaults to None
    :type profile: str, optional
    :return: A ``Session`` based on the provided parameters.
    :rtype: Session
    """
    return Session(region_name=aws_region, profile_name=profile)


def get_account_session(
    session: Session, account_id: str, role_name: str, aws_region: str = None
) -> Session:
    """Create an AWS ``Session`` that has assumed the specified role, in the
    specified region/account.

    AWS resources in the same or different accounts can be accessed by
    assuming an IAM role that provides access to the desired resource.
    This method is a convenience method that assumes an IAM role named
    as:

    ``arn:aws:iam::{account_id}:role/{role_name}``

    :param session: The ``Session`` to use to create the new ``Session``
    :type session: Session
    :param account_id: The account containing the IAM role to assume.
    :type account_id: str
    :param role_name: The name of the IAM role to assume.
    :type role_name: str
    :param aws_region: [description]
    :type aws_region: str
    :return: [description]
    :rtype: Session
    """
    sts_client = session.client("sts")
    chars = list("1234567890abcdefgh")
    shuffle(chars)
    results = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
        RoleSessionName=f"ToolSession-{''.join(chars)}",
    )
    session = Session(
        aws_access_key_id=results["Credentials"]["AccessKeyId"],
        aws_secret_access_key=results["Credentials"]["SecretAccessKey"],
        aws_session_token=results["Credentials"]["SessionToken"],
        region_name=aws_region,
    )
    return session


def get_deployer_target_session(
    hmd_region: str, profile: Optional[str], account: Optional[str]
):
    session = get_session(get_cloud_region(hmd_region), profile=profile)
    deployer_account_number = get_account_number(session)
    if account and account != deployer_account_number:
        session = get_account_session(
            session, account, "hmd.neuronsphere.deploy", get_cloud_region(hmd_region)
        )
    return session


def get_account_number(session: Session) -> str:
    return session.client("sts").get_caller_identity().get("Account")


def format_tags(tags: dict) -> list:
    return list(
        map(lambda tag_kv: {"Key": tag_kv[0], "Value": tag_kv[1]}, tags.items())
    )


STANDARD_ACCOUNTS = [
    "main",
    "admin",
    "grc",
    "security",
    "eng",
    "demo",
    "dev",
    "test",
    "qa",
    "prod",
    "stage",
]


def get_neuronsphere_domain(customer_code: str, environment: str) -> str:
    if environment == "prod":
        prefix = customer_code
    else:
        prefix = f"{customer_code}-{environment}".replace(".", "-")

    return (
        f"{prefix}-neuronsphere.io"
        if not prefix.endswith("neuronsphere")
        else f"{prefix}.io"
    )


def get_neuronsphere_account_name(customer_code: str, environment: str) -> str:
    engineering_account = "eng"

    if environment != engineering_account and environment in STANDARD_ACCOUNTS:
        return f"{customer_code}.neuronsphere.{environment}"
    else:
        return f"{customer_code}.{environment}.{engineering_account}"


@contextmanager
def cd(newdir: Union[str, Path]):
    """Change the working directory to execute code.

    Usage::

      with cd("a/different/directory"):
          # do some python stuff
          do_method("hi")

      # back in the original location
      keep_going()

    :param newdir: The directory
    :type newdir: [type]
    """
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def gen_password(
    length: int = 10, include_symbols=True, include_letters=True, include_numbers=True
) -> str:
    """Generate a random password.

    Generate a password that can be used when creating AWS accounts.

    :param length: The number of characters to generate, defaults to 10
    :type length: int, optional
    :return: A password of the specified length.
    :rtype: str
    """
    symbols = "_+=,.@-"
    numbers = "0123456789"
    upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_case = upper_case.lower()
    alphabet = symbols + numbers + upper_case + lower_case

    while True:
        password = "".join(secrets.choice(alphabet) for i in range(length))
        if (
            (
                all((not include_letters, not any(c.islower() for c in password)))
                or all((include_letters, any(c.islower() for c in password)))
            )
            and (
                all((not include_letters, not any(c.isupper() for c in password)))
                or all((include_letters, any(c.isupper() for c in password)))
            )
            and (
                all((not include_numbers, not any(c.isdigit() for c in password)))
                or all((include_numbers, any(c.isdigit() for c in password)))
            )
            and (
                all((not include_symbols, not any(c in symbols for c in password)))
                or all((include_symbols, any(c in symbols for c in password)))
            )
        ):
            break

    return password


def make_fibonacci(terms: int):
    """Create a fibonacci series containing the first ``terms`` terms.

    :param terms: The number of terms generate.
    :return:
    """
    assert terms >= 1, "terms must be >= 1"
    n1, n2 = 0, 1
    count = 0
    result = []
    while count < terms:
        result.append(n1)
        nth = n1 + n2
        n1 = n2
        n2 = nth
        count += 1
    return result


def fibonacci_wait(terms: int = 8, wait_factor: float = 0.5, min_wait: float = 0.5):
    """Retry the wrapped function until it's truthy.

    This method wrapper repeatedly calls the wrapped method until the
    result of the method is truthy. This method is primarily intended
    to monitor the status of an asynchronous request, such as
    some AWS resource creation APIs.

    The time between calls decreases as a Fibonacci series down to a
    minimum wait time. The idea is to check more frequently as the
    time taken to execute increases.

    Usage::

      ...
      @fibonacci_wait(terms=15, wait_factor=.75, min_wait=0.3)
      def do_wait_for_resource():
          return is_resource_ready()

      do_wait_for_resource()
      ...

    In this example, the ``do_wait_for_resource`` method will be
    called repeatedly until the ``is_resource_ready`` method returns
    ``True``.


    :param terms: The number of terms of the fibonacci series to generate
    :param wait_factor: A multiplier to apply to the series value
    :param min_wait: The minimum wait time in seconds.
    :return:
    """
    sequence = list(reversed(make_fibonacci(terms)))

    def decorator_wait(func):
        @wraps(func)
        def wrapper_wait(*args, **kwargs):
            i = 0
            while True:
                wait_value = sequence[i]
                i = i + 1 if i < len(sequence) - 1 else len(sequence)
                wait_time = max(wait_value * wait_factor, min_wait)
                sleep(wait_time)
                value = func(*args, **kwargs)
                if value:
                    return value

        return wrapper_wait

    return decorator_wait


def get_version() -> str:
    """Retrieve the HMD version for the current repository.

    The HMD version is expected to be in the file, ``./meta-data/VERSION``.
    Read and return this file.

    :return: The repository version.
    :rtype: str
    """
    if not os.path.exists("meta-data/VERSION"):
        raise Exception('No "meta-data/VERSION" file found.')

    with open("meta-data/VERSION", "r") as vfl:
        return vfl.read().strip()


def convert_arg_to_command_line(action: argparse.Action, namespace: argparse.Namespace):
    """
    Convert an argparse action and the corresponding parsed value into a
    string suitable to present back to the user.

    :param action: An ``argparse.Action`` object that describes how top parse a specific parameter.
    :param namespace: An ``argparse.Namespace`` object that contains the results of parsing a command line.
    :return: A ``str`` representation of the parameter as entered on the command line.
    """
    result = None
    if (
        action.default != "==SUPPRESS=="
        and action.help != "==SUPPRESS=="
        and not isinstance(action, argparse._SubParsersAction)
    ):
        if action.const is None or (
            action.const is not None
            and getattr(namespace, action.dest, None) != action.default
        ):
            result_parts = []
            if len(action.option_strings) > 0:
                result_parts.append(action.option_strings[-1])
            result_parts.append(getattr(namespace, action.dest, "None"))

            result = " ".join([str(p) for p in result_parts])

    return result


def convert_args_to_command_line(
    parser: ArgparseArgumentHandler,
    namespace: argparse.Namespace,
    sub_commands: List[str],
):
    """
    Reconstruct a entered command line from the ``cement`` parser handler and the resulting parsed values.
    This is used to display the full command that is executed after any defaults are applied.

    :param parser: The argparse parser after it is constructed.
    :param namespace: The parsed options.
    :param sub_commands: An ordered list of the subcommands entered in the command line.
    :return:
    """

    subparser_action = None
    result = []

    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            subparser_action = action
        arg_string = convert_arg_to_command_line(action, namespace)
        if arg_string:
            result.append(arg_string)

    sub_result = []
    if (
        sub_commands
        and subparser_action
        and subparser_action.choices
        and sub_commands[0] in subparser_action.choices
    ):
        command = sub_commands.pop(0)
        sub_result = convert_args_to_command_line(
            subparser_action.choices[command], namespace, sub_commands
        )
        sub_result = [command] + sub_result

    return result + sub_result


def _get_secret(
    secret_name: str, secret_value: str, secret_property: str = None
) -> str:
    try:
        secret_value = loads(secret_value)
    except JSONDecodeError as e:
        if secret_property:
            raise Exception(
                f"Secret, {secret_name}, is not valid json; cannot specify a property name."
            )

    if secret_property:
        if secret_property not in secret_value:
            raise Exception(
                f"Property, {secret_property}, is not in the secret value for secret, {secret_name}."
            )
        return secret_value[secret_property]
    else:
        return secret_value


def get_secret(
    session: Session,
    secret_name: str,
    secret_property: str = None,
    use_cache: bool = False,
):
    """Retrieve a secret from Secrets Manager.

    :param session: The Session to use.
    :param secret_name: The secret name.
    :param secret_property: An optional property to retrieve. The property must exist within the
                            secret.
    :param use_cache: Attempt to retrieve the secret value from the cache.
    :return:
    """
    if use_cache:
        cache = get_secret_cache(session)
        secret_value = cache.get_secret_string(secret_name)
    else:
        sm_client = session.client("secretsmanager")
        secret_value = sm_client.get_secret_value(SecretId=secret_name)["SecretString"]

    return _get_secret(secret_name, secret_value, secret_property)


def get_cached_secret(
    cache: SecretCache, secret_name: str, secret_property: str = None
):
    """Retrieve a secret from Secrets Manager.

    :param cache: The SecretCache to use.
    :param secret_name: The secret name.
    :param secret_property: An optional property to retrieve. The property must exist within the
                            secret.
    :return:
    """

    return _get_secret(
        secret_name, cache.get_secret_string(secret_name), secret_property
    )


def get_secret_cache(session: Session, options: Dict = {}) -> SecretCache:
    return SecretCache(
        config=SecretCacheConfig(**options), client=session.client("secretsmanager")
    )


def create_secret(
    session: Session,
    secret_name: str,
    secret_value: Union[str, dict],
    exists_ok: bool = False,
    tags: dict = {"ad-hoc": gen_password(include_symbols=False)},
):
    """Create a Secrets Manager secret.

    Create a secret. The value of the secret can be provided as either a ``dict`` or
    a ``str``. If it is a ``dict``, it will be converted to a ``str`` using ``json.dumps``.

    :param session: The Session to use to connect to AWS.
    :param secret_name: The name of the secret to create.
    :param secret_value: The value of the secret to create.
    :param exists_ok: Update the secret if it exists
    :param tags: Tags to be added to the secret

    :return:
    """
    sm_client = session.client("secretsmanager")
    if isinstance(secret_value, dict):
        secret_value = dumps(secret_value)
    try:
        sm_client.describe_secret(SecretId=secret_name)
    except sm_client.exceptions.ResourceNotFoundException as ex:
        sm_client.create_secret(
            Name=secret_name, SecretString=secret_value, Tags=format_tags(tags)
        )
    else:
        if exists_ok:
            sm_client.update_secret(SecretId=secret_name, SecretString=secret_value)


STANDARD_DEPLOY_PARAMETERS = {
    "instance-name": (
        ["-in", "--instance-name"],
        {
            "action": "store",
            "dest": "instance_name",
            "required": False,
            "default": os.environ.get("HMD_INSTANCE_NAME"),
        },
    ),
    "deployment-id": (
        ["-di", "--deployment-id"],
        {
            "action": "store",
            "dest": "deployment_id",
            "required": False,
            "default": os.environ.get("HMD_DID", "aaa"),
        },
    ),
    "environment": (
        ["-e", "--environment"],
        {
            "action": "store",
            "dest": "environment",
            "required": False,
            "default": os.environ.get("HMD_ENVIRONMENT"),
        },
    ),
    "account": (
        ["-a", "--account"],
        {
            "action": "store",
            "dest": "account",
            "required": False,
            "default": os.environ.get("HMD_ACCOUNT"),
        },
    ),
    "config-file": (
        ["-cf", "--config-file"],
        {"action": "store", "dest": "config_file", "required": False},
    ),
}


def get_standard_parameters(parameter_names: List[str] = []) -> List:
    if not parameter_names:
        parameter_names = [key for key in STANDARD_DEPLOY_PARAMETERS]
    invalid_parameters = [
        key for key in parameter_names if key not in STANDARD_DEPLOY_PARAMETERS
    ]
    if invalid_parameters:
        raise Exception(f"Invalid parameter names: {', '.join(invalid_parameters)}")
    return [STANDARD_DEPLOY_PARAMETERS[key] for key in parameter_names]


REGION_MAPPING = {
    "reg1": "us-west-2",
    "reg2": "us-east-2",
    "reg3": "eu-central-1",
    "reg4": "eu-west-3",
}


def get_cloud_region(hmd_region: str):
    if hmd_region not in REGION_MAPPING:
        raise Exception(f"HMD Region, {hmd_region}, is not recognized.")
    return REGION_MAPPING[hmd_region]


def is_eu_region(hmd_region: str):
    return get_cloud_region(hmd_region).startswith("eu-")


def get_datadog_api_url(hmd_region: str, use_sandbox: bool = False) -> str:
    host = "https://api.datadoghq.com"

    if use_sandbox == False:
        if is_eu_region(hmd_region):
            host = "https://app.datadoghq.eu"
        else:
            host = "https://us3.datadoghq.com"

    return host


def get_datadog_site(datadog_url: str) -> str:
    if datadog_url == "https://api.datadoghq.com":
        return "datadoghq.com"
    elif datadog_url == "https://app.datadoghq.eu":
        return "datadoghq.eu"
    elif datadog_url == "https://us3.datadoghq.com":
        return "us3.datadoghq.com"
    else:
        raise Exception(f"Can't create site from url: {datadog_url}")


def make_standard_name(
    instance_name: str,
    repo_name: str,
    deployment_id: str,
    environment: str,
    hmd_region: str,
    customer_code: str,
):
    name = "_".join(
        [
            instance_name,
            repo_name,
            deployment_id,
            environment,
            hmd_region,
            customer_code,
        ]
    )

    if len(name) >= 64:
        environment = environment[0]
        customer_code = customer_code[-1]
        name = "_".join(
            [
                instance_name,
                repo_name,
                deployment_id,
                environment,
                hmd_region,
                customer_code,
            ]
        )

    if len(name) >= 64:
        name = "_".join([instance_name, repo_name, deployment_id, hmd_region])

    return name


def read_manifest() -> Dict:
    manifest_path = Path("meta-data") / "manifest.json"
    if not os.path.exists(manifest_path):
        raise Exception(f"Project manifest file not found.")

    with open(manifest_path, "r") as fl:
        return json.load(fl)


def deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def set_pargs_value(pargs: SimpleNamespace, name: str, default: Any = None):
    if not hasattr(pargs, name):
        setattr(pargs, name, default)


def send_datadog_event(event_type: str, data: str, tags: Dict, ex=None):
    """
    Function to send events to datadog via API call. The assumption is that
    DD_BASE_URL and DD_API_KEY environment variables are available to establish the
    connection. If values are not provided, no exception is thrown but a message is
    returned indicating the event was not sent.

    tags parameter should be in the following format:
    {
        "tags": {
            "event_source": os.environ.get("HMD_REPO_NAME"),
            "event_source_version": version(os.environ.get("HMD_REPO_NAME")),
            "event_source_instance_name": os.environ.get("HMD_INSTANCE_NAME"),
            "event_source_did": os.environ.get("HMD_DID"),
            "event_source_cust_code": os.environ.get("HMD_CUSTOMER_CODE"),
            "event_source_region": os.environ.get("HMD_REGION"),
            "event_source_env": os.environ.get("HMD_ENVIRONMENT"),
        }
    }

    :param event_type: datadog event type (error, warning, success, info)
    :param data: the body of the event message
    :param ex: exception info, if sending an error event (default is None)
    :param tags: tags added to the event
    :return: response json
    """

    dd_base_url = os.environ.get("DD_BASE_URL")
    dd_api_key = os.environ.get("DD_API_KEY")
    try:
        dd_event = {
            "type": event_type,
            "title": f"{data}",
            "text": f"{data}: {ex}" if ex else f"{data}",
            "params": tags,
        }
        resp = requests.post(
            f"{dd_base_url}/apiop/send_event",
            json=dd_event,
            headers={"x-api-key": dd_api_key},
        )
        return resp.json()
    except Exception as e:
        print(f"Datadog event not sent: {e}")


def send_datadog_metric(metric_type: str, name: str, data: str, tags: Dict):
    """
    Function to send metrics to datadog via API call. The assumption is that
    DD_BASE_URL and DD_API_KEY environment variables are available to establish the
    connection. If values are not provided, no exception is thrown but a message is
    returned indicating the metric was not sent.

    tags parameter should be in the following format:
    {
        "tags": {
            "event_source": os.environ.get("HMD_REPO_NAME"),
            "event_source_version": version(os.environ.get("HMD_REPO_NAME")),
            "event_source_instance_name": os.environ.get("HMD_INSTANCE_NAME"),
            "event_source_did": os.environ.get("HMD_DID"),
            "event_source_cust_code": os.environ.get("HMD_CUSTOMER_CODE"),
            "event_source_region": os.environ.get("HMD_REGION"),
            "event_source_env": os.environ.get("HMD_ENVIRONMENT"),
        }
    }

    :param metric_type: datadog metric type (count, rate, gauge)
    :param name: the metric name
    :param data: the metric value
    :param tags: tags added to the event
    :return: response json
    """

    dd_base_url = os.environ.get("DD_BASE_URL")
    dd_api_key = os.environ.get("DD_API_KEY")
    try:
        dd_metric = {"type": metric_type, "name": name, "value": data, "params": tags}
        resp = requests.post(
            f"{dd_base_url}/apiop/send_metric",
            json=dd_metric,
            headers={"x-api-key": dd_api_key},
        )
        return resp.json()
    except Exception as e:
        print(f"Datadog metric not sent: {e}")


def hmd_env_path(assert_exists: bool = False) -> Optional[Path]:
    hmd_home = os.environ.get("HMD_HOME", None)

    if assert_exists:
        assert hmd_home, "HMD_HOME not set"

    return Path(os.path.expandvars(hmd_home)) / ".config" / "hmd.env"


def hmd_cache_folder_path(assert_exists: bool = False) -> Optional[Path]:
    hmd_home = os.environ.get("HMD_HOME", None)

    if assert_exists:
        assert hmd_home, "HMD_HOME not set"

    return Path(os.path.expandvars(hmd_home)) / ".cache"


def load_hmd_env(override=True):
    env_path = hmd_env_path()

    if env_path and env_path.exists():
        load_dotenv(dotenv_path=env_path, override=override)


def set_hmd_env(key: str, value):
    env_path = hmd_env_path()

    if not os.path.exists(env_path):
        os.makedirs(env_path.parent, exist_ok=True)
        with open(env_path, "w"):
            pass

    set_key(env_path, key, value)


def get_param_store_parameter(name: str, session: Optional[Session] = None) -> str:
    if not session:
        session = Session()

    ssm = session.client("ssm")
    response = ssm.get_parameter(Name=name)

    return response["Parameter"]["Value"]


def put_param_store_parameter(
    name: str, value: str, session: Optional[Session] = None, description: str = ""
) -> str:
    if not session:
        session = Session()

    ssm = session.client("ssm")
    ssm.put_parameter(
        Name=name,
        Description=description,
        Value=value,
        Tier="Standard",
        Type="String",
        Overwrite=True,
    )


def get_service_parameter(
    parameter_name: str,
    default_value: str = None,
    throw: bool = True,
    session: Optional[Session] = None,
):
    value = os.environ.get(parameter_name, default_value)

    if not value and throw:
        raise Exception(f"Environment variable, {parameter_name}, not populated.")
    if value and value.startswith("parameter_store:"):
        value = get_param_store_parameter(value[len("parameter_store:") :], session)

    return value


def get_env_var(env_var_name, throw=True, default=None):
    value = os.environ.get(env_var_name, default)
    if not value and throw:
        raise Exception(f"Environment variable {env_var_name} not populated.")
    return value
