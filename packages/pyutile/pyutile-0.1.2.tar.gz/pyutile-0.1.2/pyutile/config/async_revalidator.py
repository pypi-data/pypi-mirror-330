import asyncio

import yaml
from loguru import logger

from pyutile.config.validator import validate_config, ConfigModel


async def revalidate_config(path: str):
    logger.info("Asynchronously revalidating configuration at {}", path)
    try:
        with open(path, 'r') as f:
            config_data = yaml.safe_load(f)
        loop = asyncio.get_event_loop()
        # Offload the synchronous validation to a thread
        validated = await loop.run_in_executor(None, validate_config, config_data, ConfigModel)
        logger.info("Configuration revalidated successfully.")
        return validated
    except Exception as e:
        logger.error("Validation error during asynchronous revalidation: {}", e)
        raise
