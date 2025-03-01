import os
from yaml import safe_load
from hmd_cli_tools.hmd_cli_tools import hmd_cache_folder_path


HMD_TOKEN_FILENAME = "tokens.yaml"


def get_auth_token() -> str:
    """Retrieve an auth token that has been been created.

    Look first in the environment variable named HMD_AUTH_TOKEN. If not found
    there, look in the standard location used by the login CLI command.

    :return: the auth token
    :rtype: str
    """
    auth_token = os.environ.get("HMD_AUTH_TOKEN")
    if not auth_token:
        cache_folder_path = hmd_cache_folder_path(assert_exists=True)

        if os.path.exists(cache_folder_path / HMD_TOKEN_FILENAME):
            with open(cache_folder_path / HMD_TOKEN_FILENAME, "r") as tkn_fl:
                data = safe_load(tkn_fl)
                auth_token = data["login"]["access_token"]

    return auth_token
