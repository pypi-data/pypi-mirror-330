from typing import Any, Dict


class InvalidSQLConfigurationError(Exception):
    pass


class SQLConfigurationBuilder:
    def __init__(self, config: Any) -> None:
        self._config = config

    def build(self, data: Dict[str, Any]) -> None:
        self._config._sql_user_name = data.get('sql_user_name')
        self._config._sql_server_ip = data.get('sql_server_ip')
        self._config._sql_pass_word = data.get('sql_pass_word')
        self._config._connection_string = data.get('connection_string')
