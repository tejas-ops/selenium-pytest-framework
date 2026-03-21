import json
from pathlib import Path

_TEST_DATA_DIR = Path(__file__).parent.parent / "test_data"


def load_json(file_name):
    file_path = _TEST_DATA_DIR / file_name
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
