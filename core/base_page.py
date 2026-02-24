from web_ui_framework.core.wait_manager import WaitManager


class BasePage:
    """页面对象基类，封装常用浏览器与等待操作。"""

    def __init__(self, driver, timeout: int = 10):
        """
        :param driver: WebDriver 实例
        :param timeout: 默认显式等待超时时间（秒）
        """
        self.driver = driver
        self._timeout = timeout
        self.wait = WaitManager(driver, timeout=timeout)

    # --------- 导航与页面信息 ---------
    def open(self, url: str):
        """打开指定 URL。"""
        self.driver.get(url)

    def title(self) -> str:
        return self.driver.title

    def current_url(self) -> str:
        return self.driver.current_url

    # --------- 通用元素操作（基于定位器元组） ---------
    def find(self, locator, timeout: int | None = None):
        """等待元素可见并返回元素。"""
        if timeout is None:
            return self.wait.until_visible(locator)
        return WaitManager(self.driver, timeout=timeout).until_visible(locator)

    def find_clickable(self, locator, timeout: int | None = None):
        """等待元素可点击并返回元素。"""
        if timeout is None:
            return self.wait.until_clickable(locator)
        return WaitManager(self.driver, timeout=timeout).until_clickable(locator)

    def click(self, locator, timeout: int | None = None):
        """等待元素可点击后点击。"""
        element = self.find_clickable(locator, timeout)
        element.click()
        return element

    def type_text(self, locator, text: str, clear: bool = True, timeout: int | None = None):
        """在元素中输入文本。"""
        element = self.find(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)
        return element
