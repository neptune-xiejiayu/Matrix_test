from web_ui_framework.pages.login_page import LoginPage
from web_ui_framework.configs.config import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_placeholder_navigation(browser):
    base = settings.get("base_url")
    browser.get(base)
    lp = LoginPage(browser)
    assert lp.current_url().rstrip('/') == base.rstrip('/')


def test_login_admin_success(browser):

    home_path = "/#/homePage"
    url = settings.get("base_url")
    creds = settings.get("login", {})
    username = creds.get("username", "admin")
    password = creds.get("password", "admin")

    browser.get(url)

    wait = WebDriverWait(browser, 15)
    # 等待并输入用户名
    username_el = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_el.clear()
    username_el.send_keys(username)

    # 输入密码
    password_el = browser.find_element(By.NAME, "password")
    password_el.clear()
    password_el.send_keys(password)

    # 点击登录
    login_btn = browser.find_element(By.XPATH, "//span[contains(text(), '登录')]")
    login_btn.click()

    # 等待 URL 跳转到首页路径
    wait.until(lambda d: home_path in d.current_url, message="登录未跳转到首页")
    assert home_path in browser.current_url

    
    # 等待页面完全加载
    wati2 = WebDriverWait(browser, 10)
    act_btn = browser.find_element(By.XPATH, "//div[contains(text(),'导航到站点')]")
    act_btn.click()
    wati1 = WebDriverWait(browser, 10)
    act1_btn = browser.find_element(By.XPATH, "//span[contains(text(),'确认')]")
    act1_btn.click()