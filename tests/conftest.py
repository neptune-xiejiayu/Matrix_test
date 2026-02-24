import os
import pytest
import platform

# Tests import the framework as a package; ensure tests are executed from repository root
from web_ui_framework.configs.config import settings, load_settings
from web_ui_framework.core.browser_manager import BrowserManager


@pytest.fixture(scope="session")
def session_settings():
    """根据环境变量或操作系统自动选择配置"""
    env = os.getenv("TEST_ENV")
    if env:
        return load_settings(env)
    return settings


@pytest.fixture(scope="session")
def base_url(session_settings):
    """提供当前环境下的 base_url。"""
    return session_settings.get("base_url")


@pytest.fixture(scope="session")
def login_credentials(session_settings):
    """提供当前环境下的登录账号信息。"""
    return session_settings.get("login", {})


@pytest.fixture(scope="function")
def browser(session_settings):
    """创建浏览器实例，支持跨平台配置，并应用隐式等待。"""
    headless = session_settings.get("headless", platform.system().lower() == "linux")
    window_size = session_settings.get("window_size", "1920,1080")
    implicit_wait = session_settings.get("implicit_wait", 5)

    # 从配置中传入chromedriver路径（如果有），空字符串转换为None
    chromedriver_path = session_settings.get("chromedriver_path") if isinstance(session_settings, dict) else None
    if chromedriver_path == "":
        chromedriver_path = None

    bm = BrowserManager(headless=headless, window_size=window_size, chromedriver_path=chromedriver_path)
    driver = bm.start()

    # 统一应用隐式等待，避免测试中到处散落 driver.implicitly_wait 调用
    try:
        driver.implicitly_wait(implicit_wait)
    except Exception:
        # 在极端情况下（驱动启动失败等）不阻断测试框架的清理逻辑
        pass

    yield driver
    bm.quit()
