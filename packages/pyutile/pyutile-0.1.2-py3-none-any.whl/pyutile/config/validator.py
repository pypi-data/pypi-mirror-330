from pydantic import BaseModel, ValidationError
from typing import Any, Dict

# Example configuration model; users can extend this model.
class ConfigModel(BaseModel):
    app_name: str = "MyApp"
    database: Dict[str, Any] = {}
    logging: Dict[str, Any] = {"level": "INFO", "handlers": []}

def validate_config(config: Dict[str, Any], model: BaseModel = ConfigModel) -> BaseModel:
    """
    Validate a configuration dictionary against the provided Pydantic model.
    Raises ValueError if validation fails.
    """
    try:
        validated_config = model(**config)
        return validated_config
    except ValidationError as e:
        raise ValueError(f"Configuration validation error: {e}")

def generate_docs(model: BaseModel = ConfigModel) -> str:
    """
    Generate JSON schema documentation for the configuration model.
    """
    return model.schema_json(indent=2)
