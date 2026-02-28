from web_ui_framework.core.base_page import BasePage
from web_ui_framework.core.element_locator import ElementLocator


class DashboardPage(BasePage):
    """仪表盘页面对象，封装常用操作。"""

    welcome_banner = ElementLocator.by_css(".welcome-banner")
    user_menu = ElementLocator.by_css(".user-menu")
    logout_button = ElementLocator.by_css(".user-menu .logout")
    widgets = ElementLocator.by_css(".widget")

    def is_loaded(self) -> bool:
        return "Dashboard" in self.title()

    def get_welcome_text(self) -> str:
        el = self.find(self.welcome_banner)
        return el.text if el is not None else ""

    def open_user_menu(self, timeout: int = 10):
        self.click(self.user_menu, timeout=timeout)

    def logout(self, timeout: int = 10):
        self.open_user_menu(timeout=timeout)
        self.click(self.logout_button, timeout=timeout)

    def widget_count(self) -> int:
        return len(self.find_all(self.widgets))

    # 常用页面动作示例：用于将原测试中的 XPath 操作抽象到页面层
    navigate_button = ElementLocator.by_xpath("//div[contains(text(),'导航到站点')]")
    confirm_button = ElementLocator.by_xpath("//span[contains(text(),'确认')]")

    def navigate_to_site(self, timeout: int = 10):
        self.click(self.navigate_button, timeout=timeout)

    def confirm_action(self, timeout: int = 10):
        self.click(self.confirm_button, timeout=timeout)
