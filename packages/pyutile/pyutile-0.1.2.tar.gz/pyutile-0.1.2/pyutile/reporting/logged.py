from loguru import logger
from pyutile.config import settings
from pyutile.reporting import alerting
import sys

class Logged:
    """Manages structured logging for PyUtil using Loguru,
    configured via pyutile.config. Provides dynamic log level changes,
    structured JSON logging, and alerting integration.
    """

    def __init__(self):
        self._current_log_level = None
        self._configure_logging()

    def _configure_logging(self):
        """Loads logging settings from pyutile.config and applies them to Loguru."""
        log_config = settings.settings.get("logging", {})

        # Use dynamic override if set; otherwise, default from config.
        log_level = self._current_log_level if self._current_log_level else log_config.get("level", "INFO").upper()
        log_format = log_config.get(
            "format",
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )

        # Remove all previously added sinks.
        logger.remove()

        # Console Logging
        if log_config.get("console", True):
            logger.add(sys.stderr, format=log_format, level=log_level, enqueue=True, colorize=True)

        # File Logging
        if log_config.get("file_logging", False):
            log_file = log_config.get("file_path", "logs/pyutile.log")
            logger.add(log_file, rotation="10MB", retention="7 days", level=log_level, format=log_format, enqueue=True)

        # Structured JSON Logging
        if log_config.get("json_logging", False):
            json_file = log_config.get("json_file_path", "logs/pyutile.json")
            logger.add(json_file, rotation="10MB", retention="7 days", level=log_level, serialize=True, enqueue=True)

        # Alerting Integration: trigger external alerts for ERROR and CRITICAL logs.
        if log_config.get("alerting", False):
            logger.add(alerting.alert_sink, level="ERROR", enqueue=True)

    def set_log_level(self, new_level: str):
        """Dynamically changes the log level at runtime."""
        self._current_log_level = new_level.upper()
        self._configure_logging()

    def get_logger(self):
        """Returns the configured Loguru logger."""
        return logger

# Instantiate logging manager and expose the logger instance.
log_manager = Logged()
log = log_manager.get_logger()