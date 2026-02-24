import sys
import os
import types
import pytest

# When running from repository root, `web_ui_framework` is an importable package.
from web_ui_framework.core.browser_manager import BrowserManager
from web_ui_framework.configs.config import settings


@pytest.fixture(scope="function")
def driver():
    bm = BrowserManager(headless=settings.get("headless", False), window_size=settings.get("window_size", "1920,1080"))
    drv = bm.start()
    yield drv
    try:
        bm.quit()
    except Exception:
        pass
