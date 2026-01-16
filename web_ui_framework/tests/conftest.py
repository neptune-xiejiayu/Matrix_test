import os
import pytest

# Tests import the framework as a package; ensure tests are executed from repository root
from web_ui_framework.configs.config import settings
from web_ui_framework.core.browser_manager import BrowserManager


@pytest.fixture(scope="session")
def session_settings():
    return settings


@pytest.fixture(scope="function")
def browser(session_settings):
    bm = BrowserManager(headless=session_settings.get("headless", False), window_size=session_settings.get("window_size", "1920,1080"))
    driver = bm.start()
    yield driver
    bm.quit()
