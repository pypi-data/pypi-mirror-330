import os

class EnvironmentConfig:
    """

    """
    def __init__(self, env_var="APP_ENV"):
        self.env = os.getenv(env_var, "development")

    def get_env(self):
        """Return the current environment."""
        return self.env

    def get_config_path(self):
        """Return a config file path based on the environment."""
        return f"config_{self.env}.yaml"
