from typing import Any, Dict


class InvalidRedisConfigurationError(Exception):
    pass


class RedisConfigurationBuilder:
    def __init__(self, config: Any) -> None:
        self._config = config

    def build(self, data: Dict[str, Any]) -> None:
        self._config._redis_host = data.get('redis_host')
