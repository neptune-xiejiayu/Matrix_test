from web_ui_framework.pages.login_page import LoginPage
from web_ui_framework.pages.dashboard_page import DashboardPage


def test_placeholder_navigation(browser, base_url):
    """简单验证首页可访问性与基本跳转。"""
    browser.get(base_url)
    lp = LoginPage(browser)
    assert lp.current_url().rstrip("/") == base_url.rstrip("/")


def test_login_admin_success(browser, base_url, login_credentials):
    """验证使用配置中的管理员账号登录成功并可进入站点导航流程。"""
    home_path = "/#/homePage"
    username = login_credentials.get("username", "admin")
    password = login_credentials.get("password", "admin")

    browser.get(base_url)

    lp = LoginPage(browser)
    # 使用页面对象的登录封装并等待跳转
    lp.login_and_wait_for_home(username, password, home_path)

    # 使用 DashboardPage 的动作来替换测试里的原始 XPath 操作
    dp = DashboardPage(browser)
    dp.navigate_to_site()
    dp.confirm_action()