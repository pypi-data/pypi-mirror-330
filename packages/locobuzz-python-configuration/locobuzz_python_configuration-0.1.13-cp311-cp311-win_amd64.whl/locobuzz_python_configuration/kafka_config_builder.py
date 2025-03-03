from typing import Any, Dict


class InvalidKafkaConfigurationError(Exception):
    pass


class KafkaConfigurationBuilder:
    def __init__(self, config: Any) -> None:
        self._config = config

    def build(self, data: Dict[str, Any]) -> None:
        self._config._broker = data.get('broker')
        self._config._push_topic = data.get('push_topic')
        self._config._read_topic = data.get('read_topic')
        self._config._dead_letter_topic_name = data.get('dead_letter_topic_name')
