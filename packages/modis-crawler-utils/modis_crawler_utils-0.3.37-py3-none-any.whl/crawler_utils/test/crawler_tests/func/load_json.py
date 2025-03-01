import json
from pathlib import Path
from typing import Dict, Any
import os



def load_json_data(json_path: Path) -> Dict[str, Any]:
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"File '{json_path}' not found.")
    if os.path.getsize(json_path) == 0:
        return {}
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

