import json
import os

PATH = "data/daily_settings.json"


def load_settings():
    if not os.path.exists(PATH):
        return {}

    with open(PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_settings(data: dict):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)