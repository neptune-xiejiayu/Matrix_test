#!/usr/bin/env python3
"""
环境验证脚本
检查当前环境是否满足UI自动化测试框架的运行要求
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"✓ Python版本: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python版本兼容")
        return True
    else:
        print("✗ Python版本需要3.8或更高")
        return False


def check_dependencies():
    """检查依赖包"""
    required_packages = [
        ('selenium', 'selenium'),
        ('pytest', 'pytest'),
        ('pyyaml', 'yaml'),
    ]

    optional_packages = [
        ('allure-pytest', 'allure_pytest'),
        ('pytest-html', 'pytest_html')
    ]

    missing_required = []
    missing_optional = []

    # 检查必需包
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name} 已安装")
        except ImportError:
            missing_required.append(package_name)
            print(f"✗ {package_name} 未安装")

    # 检查可选包
    for package_name, import_name in optional_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name} 已安装")
        except ImportError:
            missing_optional.append(package_name)
            print(f"⚠ {package_name} 未安装（可选，用于增强报告功能）")

    return len(missing_required) == 0


def check_chrome_driver():
    """检查Chrome驱动"""
    system = platform.system().lower()

    # 检查环境变量
    chromedriver_env = os.getenv("CHROMEDRIVER_PATH")
    if chromedriver_env and os.path.exists(chromedriver_env):
        print(f"✓ Chrome驱动环境变量已设置: {chromedriver_env}")
        return True

    # 检查drivers目录
    root_dir = Path(__file__).parent
    drivers_dir = root_dir / "drivers"

    if system == "windows":
        driver_names = ["chromedriver.exe"]
    else:
        driver_names = ["chromedriver", "chromedriver/chromedriver"]

    for driver_name in driver_names:
        driver_path = drivers_dir / driver_name
        if driver_path.exists():
            print(f"✓ Chrome驱动已找到: {driver_path}")
            return True

    print("⚠ Chrome驱动未找到，将尝试使用系统PATH中的驱动")
    return True  # 不算错误，selenium会自动尝试


def check_chrome_browser():
    """检查Chrome浏览器"""
    system = platform.system().lower()

    if system == "linux":
        # Linux下检查chromium或google-chrome
        browsers = ["chromium-browser", "google-chrome", "chromium"]
        for browser in browsers:
            try:
                result = subprocess.run([browser, "--version"],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✓ Chrome浏览器已安装: {browser}")
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

        print("✗ 未找到Chrome浏览器，请安装chromium-browser或google-chrome")
        return False
    else:
        print("✓ 假设Windows/macOS环境下Chrome浏览器已安装")
        return True


def check_config():
    """检查配置文件"""
    config_file = Path(__file__).parent / "configs" / "settings.yaml"
    if config_file.exists():
        print(f"✓ 配置文件存在: {config_file}")
        return True
    else:
        print(f"✗ 配置文件不存在: {config_file}")
        return False


def main():
    """主验证函数"""
    print("🔍 UI自动化测试框架环境验证")
    print("=" * 50)

    system = platform.system()
    print(f"操作系统: {system}")
    print(f"架构: {platform.machine()}")
    print()

    checks = [
        ("Python版本", check_python_version),
        ("依赖包", check_dependencies),
        ("Chrome驱动", check_chrome_driver),
        ("Chrome浏览器", check_chrome_browser),
        ("配置文件", check_config),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n📋 检查{name}:")
        result = check_func()
        results.append(result)

    print("\n" + "=" * 50)
    if all(results):
        print("🎉 环境验证通过！框架可以在此环境中运行。")
        if system.lower() == "linux":
            print("💡 Linux环境建议：")
            print("   - 使用 Jenkinsfile.linux 进行CI构建")
            print("   - 设置 TEST_ENV=linux 环境变量")
            print("   - 确保系统已安装必要的依赖")
        return 0
    else:
        print("❌ 环境验证失败，请修复上述问题后再运行测试。")
        return 1


if __name__ == "__main__":
    sys.exit(main())