from web_ui_framework.core.base_page import BasePage
from web_ui_framework.core.element_locator import ElementLocator


class LoginPage(BasePage):
    """登录页面对象，封装与登录相关的元素与操作。"""

    # 定位器集中管理，测试调用页面方法而不直接使用定位器
    username = ElementLocator.by_name("username")
    password = ElementLocator.by_name("password")
    submit = ElementLocator.by_xpath("//span[contains(text(), '登录')]")
    error_msg = ElementLocator.by_css(".error")

    def open(self, url: str | None = None):
        """打开指定 URL，若未指定则刷新当前页面。"""
        if url:
            self.driver.get(url)
        else:
            self.driver.get(self.driver.current_url)

    def enter_username(self, user: str, timeout: int = 10):
        self.type_text(self.username, user, timeout=timeout)

    def enter_password(self, pwd: str, timeout: int = 10):
        self.type_text(self.password, pwd, timeout=timeout)

    def click_login(self, timeout: int = 10):
        self.click(self.submit, timeout=timeout)

    def login(self, user: str, pwd: str, timeout: int = 10):
        self.enter_username(user, timeout=timeout)
        self.enter_password(pwd, timeout=timeout)
        self.click_login(timeout=timeout)

    def login_and_wait_for_home(self, user: str, pwd: str, home_path: str, timeout: int = 15):
        """完整的登录操作并等待 URL 跳转到包含 `home_path` 的地址。"""
        self.login(user, pwd)
        return self.wait_for_url_contains(home_path, timeout=timeout)

    def get_error(self) -> str:
        els = self.driver.find_elements(*self.error_msg)
        return els[0].text if els else ""

    def is_logged_in(self) -> bool:
        return "dashboard" in self.driver.current_url.lower()
