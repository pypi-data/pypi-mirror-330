import json
import aiohttp
import aioredis
from loguru import logger
import aiobotocore

class AsyncRemoteConfigProvider:
    """
    Async provider for remote configurations.
    Supported sources: "redis", "http", "aws_ssm".
    """
    def __init__(self, source, **kwargs):
        self.source = source
        self.config_data = {}
        self.kwargs = kwargs
        if source not in ["redis", "http", "aws_ssm"]:
            raise ValueError("AsyncRemoteConfigProvider supports only 'redis', 'http', and 'aws_ssm' sources.")
        logger.info("Initialized AsyncRemoteConfigProvider with source: {}", source)

    async def fetch(self):
        if self.source == "http":
            url = self.kwargs.get("url")
            if not url:
                raise ValueError("HTTP source requires a 'url' parameter.")
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        self.config_data = await response.json()
                        logger.info("Fetched configuration via HTTP from {}", url)
                    else:
                        logger.error("HTTP request failed with status {}", response.status)
                        self.config_data = {}
        elif self.source == "redis":
            redis_url = self.kwargs.get("redis_url", "redis://localhost")
            redis_key = self.kwargs.get("redis_key", "app_config")
            redis_client = await aioredis.from_url(redis_url)
            data = await redis_client.get(redis_key)
            if data:
                self.config_data = json.loads(data.decode())
                logger.info("Fetched configuration from Redis key '{}' at {}", redis_key, redis_url)
            else:
                self.config_data = {}
        elif self.source == "aws_ssm":
            region_name = self.kwargs.get("region_name", "us-east-1")
            path = self.kwargs.get("path", "/myapp/")
            session = aiobotocore.get_session()
            async with session.create_client('ssm', region_name=region_name) as client:
                paginator = client.get_paginator("get_parameters_by_path")
                async for page in paginator.paginate(Path=path, Recursive=True, WithDecryption=True):
                    for param in page.get("Parameters", []):
                        self.config_data[param["Name"]] = param["Value"]
                logger.info("Fetched configuration from AWS SSM at path {} in region {}", path, region_name)
        return self.config_data