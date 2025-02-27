import os
import shutil
import click
import yaml
from loguru import logger
from pyutile.config.settings import Settings
from pyutile.config.secure_settings import SecureConfig

@click.group()
def cli():
    """PyUtil Configuration CLI."""
    pass

@cli.command()
@click.option('--config', required=True, help="Path to the configuration file.")
def view(config):
    """View the current configuration."""
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
        click.echo(yaml.dump(config_data))
        logger.info("Displayed configuration from {}", config)
    except Exception as e:
        logger.error("Error reading configuration: {}", e)
        click.echo(f"Error reading configuration: {e}")

@cli.command()
@click.option('--config', required=True, help="Path to the configuration file.")
@click.option('--key', required=True, help="Configuration key to update (dot notation).")
@click.option('--value', required=True, help="New value for the configuration key.")
def update(config, key, value):
    """Update a configuration key with a new value."""
    try:
        # Create a backup before updating.
        backup_path = config + ".bak"
        shutil.copyfile(config, backup_path)
        logger.info("Backup created at {}", backup_path)

        settings = Settings(config_paths=[config])
        settings.load()
        settings.set(key, value)
        settings.save(config)
        click.echo(f"Updated '{key}' to '{value}' in {config}.")
        logger.info("Updated key '{}' to '{}' in configuration.", key, value)
    except Exception as e:
        logger.error("Error updating configuration: {}", e)
        click.echo(f"Error updating configuration: {e}")

@cli.command()
@click.option('--config', required=True, help="Path to the configuration file.")
def validate(config):
    """Validate the configuration using the Pydantic model."""
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
        from pyutile.config.validator import validate_config, ConfigModel
        validate_config(config_data, ConfigModel)
        click.echo("Configuration is valid!")
        logger.info("Configuration validation successful for {}", config)
    except Exception as e:
        logger.error("Validation error: {}", e)
        click.echo(f"Validation error: {e}")

@cli.command()
def docs():
    """Generate and display the configuration documentation (JSON schema)."""
    from pyutile.config.validator import generate_docs, ConfigModel
    docs_json = generate_docs(ConfigModel)
    click.echo(docs_json)
    logger.info("Generated configuration documentation.")

@cli.command()
@click.option('--value', required=True, help="Plaintext value to encrypt.")
@click.option('--key', required=False, help="Encryption key (optional, else from CONFIG_ENCRYPTION_KEY).")
def encrypt(value, key):
    """Encrypt a plaintext value using the configured encryption key."""
    try:
        enc_key = key or os.getenv("CONFIG_ENCRYPTION_KEY")
        if not enc_key:
            raise ValueError("Encryption key must be provided or set in CONFIG_ENCRYPTION_KEY environment variable.")
        secure = SecureConfig(config_paths=[], encryption_key=enc_key)
        encrypted = secure.encrypt_value(value)
        click.echo(f"Encrypted value: {encrypted}")
        logger.info("Value encrypted successfully.")
    except Exception as e:
        logger.error("Encryption error: {}", e)
        click.echo(f"Encryption error: {e}")

@cli.command()
@click.option('--value', required=True, help="Encrypted value to decrypt.")
@click.option('--key', required=False, help="Encryption key (optional, else from CONFIG_ENCRYPTION_KEY).")
def decrypt(value, key):
    """Decrypt an encrypted value using the configured encryption key."""
    try:
        enc_key = key or os.getenv("CONFIG_ENCRYPTION_KEY")
        if not enc_key:
            raise ValueError("Encryption key must be provided or set in CONFIG_ENCRYPTION_KEY environment variable.")
        secure = SecureConfig(config_paths=[], encryption_key=enc_key)
        decrypted = secure.decrypt_value(value)
        click.echo(f"Decrypted value: {decrypted}")
        logger.info("Value decrypted successfully.")
    except Exception as e:
        logger.error("Decryption error: {}", e)
        click.echo(f"Decryption error: {e}")

@cli.command()
@click.option('--config', required=True, help="Path to the configuration file.")
@click.option('--updates', required=True, help="Path to a YAML file containing bulk updates.")
def bulk_update(config, updates):
    """Perform a bulk update of configuration keys using a YAML file."""
    try:
        # Create a backup before updating.
        backup_path = config + ".bak"
        shutil.copyfile(config, backup_path)
        logger.info("Backup created at {}", backup_path)

        with open(updates, 'r') as f:
            update_data = yaml.safe_load(f)

        settings = Settings(config_paths=[config])
        settings.load()
        for key, value in update_data.items():
            settings.set(key, value)
            logger.info("Bulk update: key '{}' updated to '{}'", key, value)
        settings.save(config)
        click.echo(f"Bulk update applied from {updates} to {config}.")
    except Exception as e:
        logger.error("Bulk update error: {}", e)
        click.echo(f"Bulk update error: {e}")

@cli.command()
@click.option('--config', required=True, help="Path to the configuration file.")
def rollback(config):
    """Rollback the configuration to the last backup."""
    backup_path = config + ".bak"
    try:
        if not os.path.exists(backup_path):
            raise FileNotFoundError("No backup configuration found.")
        shutil.copyfile(backup_path, config)
        click.echo(f"Rolled back configuration from {backup_path} to {config}.")
        logger.info("Configuration rolled back from {} to {}", backup_path, config)
    except Exception as e:
        logger.error("Rollback error: {}", e)
        click.echo(f"Rollback error: {e}")

if __name__ == '__main__':
    cli()