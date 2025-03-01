from typing import Dict, List, Any

from boto3 import Session

from hmd_cli_tools.hmd_cli_tools import (
    make_standard_name,
    get_secret_cache,
    get_cached_secret,
)


def get_neptune_endpoint(
    session: Session,
    instance_name: str,
    repo_name: str,
    deployment_id: str,
    environment: str,
    hmd_region: str,
    customer_code: str,
):
    client = session.client("neptune")
    cluster_identifier = f"{make_standard_name(instance_name, repo_name, deployment_id, environment, hmd_region, customer_code)}-cluster"
    cluster_info = client.describe_db_cluster_endpoints(
        DBClusterIdentifier=cluster_identifier.replace("_", "-"),
        Filters=[{"Name": "db-cluster-endpoint-type", "Values": ["writer"]}],
    )
    return cluster_info["DBClusterEndpoints"][0]["Endpoint"]


def get_neptune_security_group(
    session: Session,
    instance_name: str,
    repo_name: str,
    deployment_id: str,
    environment: str,
    hmd_region: str,
    customer_code: str,
):
    client = session.client("neptune")
    cluster_identifier = f"{make_standard_name(instance_name, repo_name, deployment_id, environment, hmd_region, customer_code)}-cluster"
    cluster_info = client.describe_db_clusters(
        DBClusterIdentifier=cluster_identifier.replace("_", "-")
    )
    return cluster_info["DBClusters"][0]["VpcSecurityGroups"][0]["VpcSecurityGroupId"]


class DeploymentConfig:
    def __init__(self, config: Dict):
        self.config = config

    def __getitem__(self, path: str) -> Any:
        value = self._do_get_value(path)
        if not value:
            raise KeyError(path)
        return value

    def __contains__(self, item):
        return self.get(item) is not None

    def get(self, path, default=None) -> Any:
        value = self._do_get_value(path)
        if value is None:
            return default
        else:
            return value

    def _do_get_value(self, path):
        in_path = path
        details = self.config.get("details", {})

        def do_get_config_value(
            config: Dict, path: List[str], parent: str = "__base__"
        ):
            if len(path) == 1:
                field = path[0]
                if field in config:
                    return config[field]
                elif parent != "__base__" and field in details.get(parent, {}):
                    return details.get(parent)[field]
                elif field in config["dependencies"]:
                    # it is valid to have a list of dependencies of a given type...
                    dependencies = config["dependencies"][field]
                    if isinstance(dependencies, dict):
                        dependencies = [dependencies]
                    new_configs = []
                    for dependency in dependencies:
                        new_config = {key: value for key, value in dependency.items()}
                        field_config = dependency["instance_name"]
                        for key in details[field_config]:
                            new_config[key] = details[field_config][key]
                        new_config["details"] = details
                        new_configs.append(DeploymentConfig(new_config))
                    return new_configs if len(new_configs) > 1 else new_configs[0]
                else:
                    return None
            else:
                dependency = path[0]
                if dependency in config["dependencies"]:
                    return do_get_config_value(
                        config["dependencies"][dependency],
                        path[1:],
                        config["dependencies"][dependency]["instance_name"],
                    )
                else:
                    return None

        return do_get_config_value(self.config, path.split("."))


def db_secret_name_from_dependencies(
    dp_config: DeploymentConfig, environment, hmd_region, customer_code
):
    standard_name = make_standard_name(
        instance_name=dp_config["database-instance.instance_name"],
        repo_name=dp_config["database-instance.repo_name"],
        deployment_id=dp_config["database-instance.deployment_id"],
        environment=environment,
        hmd_region=hmd_region,
        customer_code=customer_code,
    )
    return f"{standard_name}_{dp_config['db_name']}"


def get_credentials_secret(
    dp_config: DeploymentConfig,
    environment,
    hmd_region,
    customer_code,
    session: Session,
):
    standard_name = make_standard_name(
        instance_name=dp_config["instance_name"],
        repo_name=dp_config["repo_name"],
        deployment_id=dp_config["deployment_id"],
        environment=environment,
        hmd_region=hmd_region,
        customer_code=customer_code,
    )

    secret_name = dp_config.get("secret_name", standard_name)
    secret = get_cached_secret(get_secret_cache(session), secret_name)

    username_prop = dp_config.get("secret_keys.username", "username")
    password_prop = dp_config.get("secret_keys.password", "password")

    return {
        "username": secret.get(username_prop),
        "password": secret.get(password_prop),
    }
