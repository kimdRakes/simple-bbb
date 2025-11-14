thonpython
import json
import logging
from typing import List, Dict

def save_json(data: List[Dict], path: str):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Failed to save JSON: {e}")