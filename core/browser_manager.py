from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os
import platform


class BrowserManager:
    def __init__(self, headless=None, window_size="1920,1080", chromedriver_path=None):
        self.system = platform.system().lower()

        # 如果没有指定headless，根据操作系统设置默认值
        if headless is None:
            self.headless = (self.system == "linux")  # Linux默认启用无头模式
        else:
            self.headless = headless

        self.window_size = window_size
        # 可通过参数或环境变量/配置指定chromedriver路径
        self.chromedriver_path = chromedriver_path
        self.driver = None

    def _configure_chrome_options(self):
        """配置Chrome选项，支持跨平台"""
        options = Options()

        # Linux特定配置
        if self.system == "linux":
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")

        # 通用配置
        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument(f"--window-size={self.window_size}")

        # 禁用Chrome的自动化提示
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        return options

    def _get_chromedriver_path(self):
        """自动检测或获取chromedriver路径"""
        # 优先使用环境变量
        chromedriver = os.getenv("CHROMEDRIVER_PATH")
        if chromedriver and os.path.exists(chromedriver):
            return chromedriver

        # 如果通过构造函数传入了路径且存在，优先使用
        if self.chromedriver_path:
            try:
                if os.path.exists(self.chromedriver_path):
                    return self.chromedriver_path
            except Exception:
                pass

        # 自动检测drivers目录中的驱动
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        drivers_dir = os.path.join(root_dir, "drivers")

        # 根据操作系统选择驱动文件名
        if self.system == "windows":
            driver_name = "chromedriver.exe"
        else:  # linux, darwin
            driver_name = "chromedriver"

        # 检查chromedriver目录
        chromedriver_dir = os.path.join(drivers_dir, "chromedriver")
        if os.path.exists(chromedriver_dir):
            driver_path = os.path.join(chromedriver_dir, driver_name)
            if os.path.exists(driver_path):
                return driver_path

        # 检查根目录drivers
        driver_path = os.path.join(drivers_dir, driver_name)
        if os.path.exists(driver_path):
            return driver_path

        # 如果都没找到，返回None让selenium自动查找
        return None

    def start(self):
        options = self._configure_chrome_options()

        chromedriver_path = self._get_chromedriver_path()
        if chromedriver_path:
            service = ChromeService(chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            self.driver = webdriver.Chrome(options=options)

        # 执行JavaScript隐藏webdriver痕迹
        if self.driver:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return self.driver

    def quit(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
