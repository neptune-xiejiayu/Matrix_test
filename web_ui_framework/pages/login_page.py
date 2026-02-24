from web_ui_framework.core.base_page import BasePage
from web_ui_framework.core.element_locator import ElementLocator


class LoginPage(BasePage):
    username = ElementLocator.by_name("username")
    password = ElementLocator.by_name("password")
    submit = ElementLocator.by_css("button[type=submit]")
    error_msg = ElementLocator.by_css(".error")

    def open(self):
        self.driver.get(self.driver.current_url)

    def login(self, user, pwd):
        u = self.driver.find_element(*self.username)
        u.clear()
        u.send_keys(user)
        p = self.driver.find_element(*self.password)
        p.clear()
        p.send_keys(pwd)
        self.driver.find_element(*self.submit).click()

    def get_error(self):
        els = self.driver.find_elements(*self.error_msg)
        return els[0].text if els else ""

    def is_logged_in(self):
        return "dashboard" in self.driver.current_url.lower()
