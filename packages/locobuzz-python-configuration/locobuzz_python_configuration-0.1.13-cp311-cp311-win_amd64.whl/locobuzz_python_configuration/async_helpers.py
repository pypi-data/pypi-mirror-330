# async_helpers.py
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional, List

from locobuzz_python_configuration.redis_client import RedisClientFactory
from locobuzz_python_configuration.logger_config import setup_logger
from locobuzz_python_configuration.utils_functions import setup_google_chat_messenger


@dataclass
class LoggerConfig:
    logger: Any
    log_enabled: List[str]

    def __iter__(self):
        yield self.logger
        yield self.log_enabled


async def configure_logger(service_name: str, configuration: Dict[str, Any]) -> LoggerConfig:
    is_async_logger = configuration.get('_is_async_logger', False)
    log_level = configuration['_log_level']
    logger = setup_logger(service_name, async_mode=is_async_logger, log_level_str=log_level)
    logger.info("Logger configured" + (" in async mode" if is_async_logger else ""))
    log_enabled = configuration.get('_log_enabled', "PRODUCTION").split(",")
    logger.info(f"Log enabled for environment: {log_enabled}")
    return LoggerConfig(logger=logger, log_enabled=log_enabled)


@dataclass
class GoogleChatConfig:
    g_chat: Any

    def __iter__(self):
        yield self.g_chat


async def configure_google_chat(service_name: str, configuration: Dict[str, Any],
                                environ: Any, log_enabled: List[str], logger: Any) -> GoogleChatConfig:
    extra_properties = configuration.get('_extra_properties', {})
    is_async_gchat = extra_properties.get("is_async_gchat", False)
    g_chat_hook = extra_properties.get("g_chat_webhook")
    error_gchat_hook = extra_properties.get("error_g_chat_webhook")
    logger.info(f"Google Chat async mode: {is_async_gchat}")
    g_chat = setup_google_chat_messenger(
        service_name, g_chat_hook, error_gchat_hook, environ,
        is_async_gchat, log_enabled, logger
    )
    return GoogleChatConfig(g_chat=g_chat)


@dataclass
class ClickHouseConfig:
    host: Any
    port: Any
    password: Any
    username: Any

    def __iter__(self):
        yield self.host
        yield self.port
        yield self.password
        yield self.username


async def configure_clickhouse(configuration: Dict[str, Any]) -> ClickHouseConfig:
    clickhouse_username = configuration.get('_clickhouse_username', None)
    clickhouse_password = configuration.get('_clickhouse_password', None)
    clickhouse_host = configuration.get('_clickhouse_host')
    clickhouse_port = configuration.get('_clickhouse_port')
    return ClickHouseConfig(
        host=clickhouse_host,
        port=clickhouse_port,
        password=clickhouse_password,
        username=clickhouse_username
    )


@dataclass
class KafkaConfig:
    broker: Any
    read_topic: Any
    push_topic: Optional[Any]
    consumer_group_id: Optional[Any]

    def __iter__(self):
        yield self.broker
        yield self.read_topic
        yield self.push_topic
        yield self.consumer_group_id


async def configuration_kafka(configuration: Dict[str, Any]) -> KafkaConfig:
    broker = configuration['_broker']
    read_topic = configuration['_read_topic']
    push_topic = configuration.get("_push_topic")
    consumer_group_id = configuration.get("_extra_properties", {}).get("consumer_group_id")
    return KafkaConfig(
        broker=broker,
        read_topic=read_topic,
        push_topic=push_topic,
        consumer_group_id=consumer_group_id
    )





# --- New MySQL Auth Helper ---
@dataclass
class MySQLConfig:
    host: Any
    port: Any
    username: Any
    password: Any
    database: Any

    def __iter__(self):
        yield self.host
        yield self.port
        yield self.username
        yield self.password
        yield self.database


async def configure_mysql_auth(configuration: Dict[str, Any]) -> MySQLConfig:
    """
    Retrieves MySQL authentication details from the configuration.
    Expected keys: _mysql_host, _mysql_port, _mysql_username, _mysql_password, _mysql_database.
    """
    mysql_host = configuration.get('_mysql_host')
    mysql_port = configuration.get('_mysql_port')
    mysql_username = configuration.get('_mysql_username')
    mysql_password = configuration.get('_mysql_password')
    mysql_database = configuration.get('_mysql_database')
    return MySQLConfig(
        host=mysql_host,
        port=mysql_port,
        username=mysql_username,
        password=mysql_password,
        database=mysql_database
    )


@dataclass
class RedisConfig:
    redis_obj: Any

    def __iter__(self):
        yield self.redis_obj


def configure_redis(configuration: Dict[str, Any], environ: Any, logger: Any, client_type: int = 1, decode_responses: bool = False) -> RedisConfig:
    # Extract the client type as an integer: 1 for simple, 2 for advanced (default is 1)
    # Extract decode_responses flag (default False)
    redis_obj = None
    redis_url = configuration.get("_redis_host")
    if redis_url and redis_url not in {"REDIS_SERVER", "", " "}:

        redis_obj = RedisClientFactory.create(redis_url, environ, client_type, logger, decode_responses)
        if not redis_obj:
            logger.warning("Exception while initializing the redis")
            sys.exit(0)
    return RedisConfig(redis_obj=redis_obj)