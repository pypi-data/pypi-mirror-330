import yaml
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class ServerConfig:
    api_base: str
    ws_base: str
    upload_path: str
    translate_path: str
    download_path: str
    ws_path: str
    websocket_timeout: int

@dataclass(frozen=True)
class RetryConfig:
    websocket_reconnect_attempts: int

# Load configuration from YAML file
_config_path = Path(__file__).parent / "config.yml"
with _config_path.open() as f:
    _config_data = yaml.safe_load(f)

SERVER_CONF = ServerConfig(**_config_data['server'])
RETRY_CONF = RetryConfig(**_config_data['retry'])
PREFIX = _config_data.get('prefix', 'fa - ')