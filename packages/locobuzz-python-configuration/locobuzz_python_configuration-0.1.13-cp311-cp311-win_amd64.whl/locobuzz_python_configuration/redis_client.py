# redis_client.py
from typing import Union

import redis
from redis.cluster import RedisCluster as RedisClusterClient


# --- Simple Implementation ---
def initialize_redis(url: str, environ: str, logger=None, decode_responses: bool = True):
    """
    Simple Redis initialization.
    If a logger is not provided, it will use the default logger from logger_util.
    """

    if environ.lower() == "production":
        logger.info(f"Url received for redis prod is {url}")
        split_url, port_str = url.split(':')
        try:
            port = int(port_str)
        except ValueError:
            port = 6379
        logger.info(f"After splitting {split_url}")
        redis_client = RedisClusterClient(host=split_url, port=port, decode_responses=decode_responses)
        logger.info(redis_client.get_nodes())
        logger.info("Connection to redis is successful")
        return redis_client
    else:
        redis_client = redis.Redis.from_url(url=f"redis://{url}", decode_responses=decode_responses)
        return redis_client


# --- Advanced Implementation ---
class IRedisClient:
    """Interface for Redis clients."""

    def get(self, key: str) -> Union[str, None]:
        raise NotImplementedError

    def set(self, key: str, value: str, ex: int = 0) -> bool:
        raise NotImplementedError

    def delete(self, key: str) -> bool:
        raise NotImplementedError

    def increment_category_counts(self, operation_id: str, batch_data: list):
        raise NotImplementedError


class BaseRedisClient(IRedisClient):
    """Base Redis client with common functionality and error handling."""
    DEFAULT_TTL = 604800  # 7 days in seconds

    def __init__(self, url: str, logger: any, decode_responses: bool = True):
        self.url = url
        self.logger = logger
        self.decode_responses = decode_responses
        self.client = self.connect()

    def connect(self):
        """Override this method in subclasses to implement connection logic."""
        raise NotImplementedError

    def get(self, key: str) -> Union[str, None]:
        try:
            return self.client.get(key)
        except Exception as e:
            self.logger.error(f"Error getting key '{key}': {e}")
            return None

    def set(self, key: str, value: str, ex: int = 0) -> bool:
        try:
            ttl = ex if ex != 0 else self.DEFAULT_TTL
            return self.client.set(key, value, ex=ttl)
        except Exception as e:
            self.logger.error(f"Error setting key '{key}': {e}")
            return False

    def delete(self, key: str) -> bool:
        try:
            return self.client.delete(key)
        except Exception as e:
            self.logger.error(f"Error deleting key '{key}': {e}")
            return False

    def increment_category_counts(self, operation_id: str, batch_data: list):
        redis_key = f"Mod:RetagOperations:{operation_id}:category_counts"
        try:
            pipeline = self.client.pipeline()
            pipeline.expire(redis_key, 10800)
            for category in batch_data:
                category_id = str(category.get('id'))
                pipeline.hincrby(redis_key, category_id, 1)
                for subcategory in category.get('subCategories', []):
                    subcategory_id = str(subcategory.get('id'))
                    pipeline.hincrby(redis_key, subcategory_id, 1)
                    for subsubcategory in subcategory.get('subSubCategories', []):
                        subsubcategory_id = str(subsubcategory.get('id'))
                        pipeline.hincrby(redis_key, subsubcategory_id, 1)
            pipeline.execute()
        except Exception as e:
            self.logger.error(f"Error incrementing category counts for operation '{operation_id}': {e}")


class ProductionRedisClient(BaseRedisClient):
    """Production Redis client using Redis Cluster."""

    def connect(self):
        try:
            host, port = self._parse_url(self.url)
            return RedisClusterClient(host=host, port=port, decode_responses=self.decode_responses)
        except Exception as e:
            self.logger.error(f"Error connecting to Production Redis at '{self.url}': {e}")
            raise

    def _parse_url(self, url: str):
        parts = url.split(':')
        host = parts[0]
        port = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 6379
        return host, port


class DevelopmentRedisClient(BaseRedisClient):
    """Development Redis client using redis-py."""

    def connect(self):
        try:
            # Ensure URL is in the correct format for redis.Redis.from_url
            url = self.url if self.url.startswith("redis://") else f"redis://{self.url}"
            return redis.Redis.from_url(url, decode_responses=self.decode_responses)
        except Exception as e:
            self.logger.error(f"Error connecting to Development Redis at '{self.url}': {e}")
            raise


class RedisClientFactory:
    """Factory for creating Redis clients."""

    @staticmethod
    def create(url: str, environ: str, client_type: int = 2, logger: any = None, decode_responses: bool = True) -> \
            Union[IRedisClient, object]:
        """
        Create a Redis client instance.
        - client_type: 1 for simple implementation, 2 for advanced (default).
        """
        if client_type == 1:
            return initialize_redis(url, environ, logger, decode_responses)
        else:
            if environ.lower() == "production":
                return ProductionRedisClient(url, logger, decode_responses)
            else:
                return DevelopmentRedisClient(url, logger, decode_responses)
