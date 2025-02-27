import os
from cryptography.fernet import Fernet
import yaml
import json
from pyutile.config.settings import Settings
from omegaconf import OmegaConf
from loguru import logger

class SecureConfig(Settings):
    """
    Extends Settings to support encryption for sensitive data.
    An encryption key must be provided or set in the CONFIG_ENCRYPTION_KEY environment variable.
    """
    def __init__(self, config_paths, encryption_key=None, defaults=None):
        super().__init__(config_paths, defaults=defaults)
        self.encryption_key = encryption_key or os.getenv("CONFIG_ENCRYPTION_KEY")
        if not self.encryption_key:
            raise ValueError("Encryption key must be provided or set in environment variable CONFIG_ENCRYPTION_KEY")
        self._fernet = Fernet(self.encryption_key)
        logger.info("SecureConfig initialized with encryption key.")

    def encrypt_value(self, value: str) -> str:
        """Encrypt a configuration value."""
        encrypted = self._fernet.encrypt(value.encode()).decode()
        logger.debug("Encrypted value for sensitive data.")
        return encrypted

    def decrypt_value(self, encrypted_value: str) -> str:
        """Decrypt an encrypted configuration value."""
        decrypted = self._fernet.decrypt(encrypted_value.encode()).decode()
        logger.debug("Decrypted sensitive value.")
        return decrypted

    def get_secure(self, key, default=None):
        """Retrieve and decrypt a setting."""
        encrypted_value = self.get(key, default)
        return self.decrypt_value(encrypted_value) if encrypted_value else default

    def set_secure(self, key, value):
        """Encrypt and store a setting."""
        encrypted_val = self.encrypt_value(value)
        self.set(key, encrypted_val)

    def save(self, path, format="yaml"):
        """Save current settings (encrypted values remain encrypted)."""
        with open(path, 'w') as f:
            container = OmegaConf.to_container(self.config)
            if format == "yaml":
                yaml.dump(container, f)
            elif format == "json":
                json.dump(container, f, indent=4)
        logger.info("Secure configuration saved to {}", path)
