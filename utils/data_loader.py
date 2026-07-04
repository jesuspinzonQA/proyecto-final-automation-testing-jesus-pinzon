import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def load_json(relative_path):
    file_path = ROOT_DIR / relative_path
    with file_path.open(encoding="utf-8") as file:
        return json.load(file)
