from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os


class BrowserManager:
    def __init__(self, headless=False, window_size="1920,1080"):
        self.headless = headless
        self.window_size = window_size
        self.driver = None

    def start(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={self.window_size}")
        chromedriver = os.getenv("CHROMEDRIVER_PATH")
        if chromedriver:
            service = ChromeService(chromedriver)
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            self.driver = webdriver.Chrome(options=options)
        return self.driver

    def quit(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
