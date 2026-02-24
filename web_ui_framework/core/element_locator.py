from selenium.webdriver.common.by import By


class ElementLocator:
    @staticmethod
    def by_id(id_):
        return (By.ID, id_)

    @staticmethod
    def by_name(name):
        return (By.NAME, name)

    @staticmethod
    def by_css(selector):
        return (By.CSS_SELECTOR, selector)

    @staticmethod
    def by_xpath(xpath):
        return (By.XPATH, xpath)
