import os
import yaml

ROOT = os.path.dirname(os.path.dirname(__file__))
SETTINGS_FILE = os.path.join(ROOT, "configs", "settings.yaml")


def load_settings(env="default"):
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get(env, {})


settings = load_settings()
