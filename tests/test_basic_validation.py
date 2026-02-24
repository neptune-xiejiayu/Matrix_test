"""
基础验证测试
验证框架在Linux环境下的基本功能
"""

import pytest
from web_ui_framework.configs.config import settings, load_settings
from web_ui_framework.core.browser_manager import BrowserManager
import platform


def test_config_loading():
    """测试配置加载功能"""
    # 测试默认配置
    default_settings = load_settings()
    assert "base_url" in default_settings
    assert "headless" in default_settings

    # 测试Linux环境配置
    linux_settings = load_settings("linux")
    assert "base_url" in linux_settings
    assert linux_settings.get("headless") == True  # Linux默认启用无头模式

    # 测试Windows环境配置
    windows_settings = load_settings("windows")
    assert "base_url" in windows_settings
    assert windows_settings.get("headless") == False  # Windows默认禁用无头模式


def test_browser_manager_initialization():
    """测试浏览器管理器初始化"""
    system = platform.system().lower()

    # 测试默认配置
    bm = BrowserManager()
    assert bm.headless == (system == "linux")  # Linux默认无头
    assert bm.window_size == "1920,1080"
    assert bm.system == system

    # 测试自定义配置
    bm_custom = BrowserManager(headless=True, window_size="1280,720")
    assert bm_custom.headless == True
    assert bm_custom.window_size == "1280,720"


def test_settings_auto_detection():
    """测试操作系统自动检测"""
    system = platform.system().lower()

    # 测试自动选择环境
    auto_settings = load_settings()
    if system == "linux":
        assert auto_settings.get("headless") == True
    elif system == "windows":
        assert auto_settings.get("headless") == False


def test_chromedriver_detection():
    """测试Chrome驱动检测"""
    bm = BrowserManager()

    # 测试驱动路径检测（不实际启动浏览器）
    driver_path = bm._get_chromedriver_path()
    # 如果返回None，说明没有找到驱动但这不是错误（selenium会自动处理）
    if driver_path:
        assert driver_path.endswith("chromedriver") or driver_path.endswith("chromedriver.exe")


def test_chrome_options_configuration():
    """测试Chrome选项配置"""
    bm = BrowserManager()
    options = bm._configure_chrome_options()

    # 检查通用选项
    assert "--window-size=1920,1080" in options.arguments

    # 检查Linux特定选项
    if bm.system == "linux":
        linux_options = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--disable-software-rasterizer"]
        for option in linux_options:
            assert option in options.arguments


if __name__ == "__main__":
    pytest.main([__file__, "-v"])