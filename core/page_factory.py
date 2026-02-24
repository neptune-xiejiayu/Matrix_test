from web_ui_framework.pages.login_page import LoginPage
from web_ui_framework.pages.dashboard_page import DashboardPage


class PageFactory:
    def __init__(self, driver):
        self.driver = driver

    def login_page(self):
        return LoginPage(self.driver)

    def dashboard_page(self):
        return DashboardPage(self.driver)
