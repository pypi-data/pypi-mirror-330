import os
from configparser import NoSectionError


def get_credentials(cred_target: str, app_config: str, fail_if_not_found=True):
    """Retrieves username/password for a given target.

    Retrieves a username/password combination by looking first in
    environment variables and then in the hmd config file
    located in ``~/.hmd.yml``.

    For example, if the value of ``cred_target`` is "docker",
    get_credentials first checks the environment variables::

        DOCKER_USERNAME
        DOCKER_PASSWORD

    If the ``DOCKER_USERNAME`` environment variable is not set,
    it will then look in the ``docker.username`` and ``docker.password``
    configuration variables. These would be in the hmd config file
    as such::

        docker:
            username: <user_name>
            password: <password>

    :param cred_target: The name of the system for which credentials are desired.
    :param app_config: The Cement app configuration object, retrieved in the controller
                       like so: ``self.app.config``
    :param fail_if_not_found: Raise an exception if the configuration is not found.

    :return: A dict with keys, ``username`` and ``password``, or ``None``.

    :raise Exception: If no credentials are found and ``fail_if_not_found`` is ``True``
    """
    username = os.environ.get(f"{cred_target.upper()}_USERNAME")
    password = os.environ.get(f"{cred_target.upper()}_PASSWORD")

    if not username:
        if fail_if_not_found:
            raise Exception(f"No credentials found for {cred_target}.")
        else:
            result = None
    else:
        result = {"username": username, "password": password}
    return result
