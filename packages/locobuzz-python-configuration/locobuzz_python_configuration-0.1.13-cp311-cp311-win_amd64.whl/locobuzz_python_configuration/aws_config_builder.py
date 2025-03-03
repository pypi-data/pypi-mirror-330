from typing import Any, Dict


class InvalidAWSConfigurationError(Exception):
    pass


class AWSConfigurationBuilder:
    def __init__(self, config: Any) -> None:
        self._config = config

    def build(self, data: Dict[str, Any]) -> None:
        self._config._aws_access_key = data.get('aws_access_key')
        self._config._aws_secret_key = data.get('aws_secret_key')
