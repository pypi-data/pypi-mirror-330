from pyutile.config.settings import Settings
from pyutile.config.environment import EnvironmentConfig

# Load configuration based on environment
env_config = EnvironmentConfig()
config_path = env_config.get_config_path()

# Initialize settings
settings = Settings(config_paths=[config_path], defaults={"app_name": "MyApp"})

# Load configurations
settings.load()

# Access configurations
db_host = settings.get("database.host", "localhost")
print(f"Database Host: {db_host}")

# Update configuration
settings.set("database.host", "127.0.0.1")

# Save updated configuration
settings.save("updated_config.yaml")