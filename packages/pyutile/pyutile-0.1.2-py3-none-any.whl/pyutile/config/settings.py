import yaml
import os

from omegaconf import DictConfig


class Settings:
    """Loads configuration settings from a YAML file or environment variables."""

    def __init__(self, config_path="config.yml"):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self):
        """Loads configuration from a YAML file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f) or {}
        return {}

    def get(self, key, default=None):
        """Retrieves a configuration value."""
        return self._config.get(key, default)

    @property
    def all(self):
        all_settings = DictConfig({})
        for key in self._config.keys():
            all_settings.update(self._config.get(key))

        return all_settings

# Global settings instance
settings = Settings().all
