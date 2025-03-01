import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Loads configuration from config.json."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file '{CONFIG_FILE}' not found!")

    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    # Validate required fields
    required_keys = ["remote_host", "username", "remote_path", "local_path", "port"]
    for key in required_keys:
        if key not in config or not config[key]:
            raise ValueError(f"Missing required configuration: {key}")

    return config
