import configparser
import json
import toml
import yaml
from pathlib import Path
from loguru import logger

class ConfigLoader:
    def __init__(self, config_paths=None):
        self.config_paths = config_paths or []
        self.config_data = {}

    def load(self):
        """Load configuration from multiple sources and merge them."""
        for path in self.config_paths:
            if Path(path).exists():
                self._load_file(path)
                logger.info("Loaded configuration from {}", path)
        return self.config_data

    def _load_file(self, path):
        """Detects file type and loads the corresponding configuration."""
        ext = Path(path).suffix.lower()
        if ext in {'.ini', '.cfg'}:
            self._load_ini(path)
        elif ext == '.json':
            self._load_json(path)
        elif ext in {'.yaml', '.yml'}:
            self._load_yaml(path)
        elif ext == '.toml':
            self._load_toml(path)

    def _load_ini(self, path):
        parser = configparser.ConfigParser()
        parser.read(path)
        self.config_data.update({section: dict(parser[section]) for section in parser.sections()})

    def _load_json(self, path):
        with open(path, 'r') as f:
            self.config_data.update(json.load(f))

    def _load_yaml(self, path):
        with open(path, 'r') as f:
            self.config_data.update(yaml.safe_load(f))

    def _load_toml(self, path):
        with open(path, 'r') as f:
            self.config_data.update(toml.load(f))
