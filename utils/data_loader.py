import json
from pathlib import Path


def load_json(file_name):
    file_path = Path("test_data") / file_name
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)