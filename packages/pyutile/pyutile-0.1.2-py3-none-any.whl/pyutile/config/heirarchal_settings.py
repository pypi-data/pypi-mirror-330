from pyutile.config.settings import Settings, ConfigLoader
from omegaconf import OmegaConf
from loguru import logger

class HierarchicalSettings(Settings):
    """
    Supports multi-layered configuration:
      - Global (lowest priority)
      - Module
      - User (highest priority)
    """
    def __init__(self, global_config, module_config=None, user_config=None, defaults=None):
        self.global_config = global_config
        self.module_config = module_config
        self.user_config = user_config
        # Initialize base settings using global configuration.
        super().__init__(config_paths=[global_config], defaults=defaults)
        logger.info("HierarchicalSettings created with global: {}, module: {}, user: {}",
                    global_config, module_config, user_config)

    def load(self):
        """Load configurations with precedence: Global < Module < User."""
        # Load global configuration.
        super().load()
        # Merge module-specific configuration.
        if self.module_config:
            module_data = ConfigLoader([self.module_config]).load()
            self.config = OmegaConf.merge(self.config, module_data)
            logger.info("Module configuration merged: {}", module_data)
        # Merge user-specific configuration.
        if self.user_config:
            user_data = ConfigLoader([self.user_config]).load()
            self.config = OmegaConf.merge(self.config, user_data)
            logger.info("User configuration merged: {}", user_data)