import yaml
from pathlib import Path
from typing import Dict, Any

def load_yaml_config(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config.get("models", {})