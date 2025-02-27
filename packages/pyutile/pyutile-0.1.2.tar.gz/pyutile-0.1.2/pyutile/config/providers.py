import requests
import redis
import json

class RemoteConfigProvider:
    def __init__(self, source, **kwargs):
        self.source = source
        self.config_data = {}

        if source == "redis":
            self.client = redis.Redis(**kwargs)
        elif source == "http":
            self.url = kwargs.get("url")
        elif source == "aws_ssm":
            import boto3
            self.client = boto3.client("ssm")

    def fetch(self):
        """Fetch remote configurations from the defined source."""
        if self.source == "redis":
            self.config_data = json.loads(self.client.get("app_config") or "{}")
        elif self.source == "http":
            response = requests.get(self.url)
            self.config_data = response.json()
        elif self.source == "aws_ssm":
            response = self.client.get_parameters_by_path(Path="/myapp/")
            self.config_data = {p["Name"]: p["Value"] for p in response["Parameters"]}

        return self.config_data
