from web_ui_framework.core.base_page import BasePage
from web_ui_framework.core.element_locator import ElementLocator


class DashboardPage(BasePage):
    welcome_banner = ElementLocator.by_css(".welcome-banner")
    user_menu = ElementLocator.by_css(".user-menu")
    logout_button = ElementLocator.by_css(".user-menu .logout")
    widgets = ElementLocator.by_css(".widget")

    def is_loaded(self):
        return "Dashboard" in self.title()

    def get_welcome_text(self):
        return self.driver.find_element(*self.welcome_banner).text

    def open_user_menu(self):
        self.driver.find_element(*self.user_menu).click()

    def logout(self):
        self.open_user_menu()
        self.driver.find_element(*self.logout_button).click()

    def widget_count(self):
        return len(self.driver.find_elements(*self.widgets))
