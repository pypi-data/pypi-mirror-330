from .hmd_cli_tools import cd, get_version, load_hmd_env


class ServiceException(Exception):
    def __init__(self, message: str, status: int = 400):
        self.message = message
        self.status = status

    def __str__(self):
        return f"{self.message} ({self.status})"


class HmdEntityNotFoundException(ServiceException):
    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super(HmdEntityNotFoundException, self).__init__(
            f"No entity found for type: {entity_type} with id {entity_id}", 404
        )

    def __str__(self):
        return f"No entity found for type: {self.entity_type} with id {self.entity_id}"
