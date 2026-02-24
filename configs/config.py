import os
import yaml
import platform

ROOT = os.path.dirname(os.path.dirname(__file__))
SETTINGS_FILE = os.path.join(ROOT, "configs", "settings.yaml")


def load_settings(env=None):
    """加载配置，支持自动检测操作系统环境"""
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # 如果没有指定环境，自动根据操作系统选择
    if env is None:
        system = platform.system().lower()
        if system == "linux":
            env = "linux"
        elif system == "windows":
            env = "windows"
        else:
            env = "default"

    # 如果指定了环境变量，优先使用环境变量
    env_var = os.getenv("TEST_ENV")
    if env_var and env_var in data:
        env = env_var

    return data.get(env, data.get("default", {}))


settings = load_settings()
