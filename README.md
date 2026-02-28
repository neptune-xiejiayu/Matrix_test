# Web UI 自动化测试框架

这是一个基于 Selenium + pytest 的 Web UI 自动化测试框架示例脚手架，支持 Windows 和 Linux 环境。

## 目录结构与快速启动

### 环境验证

在运行测试前，建议先验证环境兼容性：

```bash
# Linux环境
python3 validate_environment.py

# Windows环境
python validate_environment.py
```

### 安装依赖

```bash
# Linux环境
python3 -m pip install -r requirements.txt

# Windows环境
python -m pip install -r requirements.txt
```

### 运行示例测试

```bash
# 建议在仓库根运行，使用包导入路径：
pytest -q web_ui_framework

# 指定环境运行（可选）
TEST_ENV=linux pytest -q web_ui_framework  # Linux环境
TEST_ENV=windows pytest -q web_ui_framework  # Windows环境
```

## 跨平台支持

框架已针对 Linux 和 Windows 环境进行了优化：

- **自动环境检测**：框架会自动检测操作系统并应用相应的配置
- **浏览器驱动**：支持自动检测 Windows 的 `.exe` 文件和 Linux 的二进制文件
- **Chrome选项**：Linux 环境自动添加 `--no-sandbox`、`--disable-dev-shm-usage` 等参数
- **配置管理**：支持多环境配置（`default`、`linux`、`windows`、`ci`）

## CI 配置

### Jenkins

- **Windows环境**：使用 `Jenkinsfile`
- **Linux环境**：使用 `Jenkinsfile.linux`

#### 在 Jenkins 上运行（建议）

- 在 Jenkins 中创建流水线任务，指向本仓库。
- 确保构建节点可以使用 `python3`、`pip`，并能运行浏览器或 `xvfb`（无头环境）。
- 如果 agent 没有系统级 Chrome/Chromium，你可以：
	- 安装 `google-chrome-stable` 或 `chromium-browser` 并确保 `chromedriver` 可用，或
	- 将 `CHROMEDRIVER_PATH` 环境变量设置为仓库中 `drivers/chromedriver/chromedriver` 的绝对路径。
- `Jenkinsfile.linux` 会在 CI 运行时设置 `TEST_ENV=ci` 并尝试用 `xvfb-run` 启动测试以支持无头浏览器。

示例 Jenkins 全局环境变量（可选）：

- `CHROMEDRIVER_PATH`：/usr/local/bin/chromedriver
- `TEST_ENV`：ci

### 在远程仓库启用 CI
- **GitHub**：推送到仓库并确保 `main` 或 `master` 分支存在，Actions 将自动触发
- **Jenkins**：在 Jenkins 中创建新的流水线任务并指向仓库，Jenkins 将使用相应的 `Jenkinsfile`

## Linux 环境特别说明

在 Linux CI 环境中，确保安装必要的系统依赖：

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver

# 或者安装 Google Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install -y google-chrome-stable
```

## 本地运行说明

- 推荐在仓库根目录运行测试，确保 `web_ui_framework` 包在 `PYTHONPATH` 中（`run_tests.py` 已处理此事）：

```bash
# 在仓库根运行（会把仓库根加入 sys.path）
python3 web_ui_framework/run_tests.py
# 或直接运行 pytest
pytest -q web_ui_framework
```

- 如果本地没有 chromedriver 在 PATH 中：

```bash
export CHROMEDRIVER_PATH=/path/to/chromedriver
pytest -q web_ui_framework
```

- 如果你希望本地模拟 CI（无头），可以使用 `xvfb-run`：

```bash
xvfb-run -s "-screen 0 1920x1080x24" pytest -q web_ui_framework
```

## Page Object 模式与用例编写建议

本框架采用 Page Object 模式：页面定位器与操作封装在 `pages/`，测试用例只调用页面方法以保持清晰和可维护。

- 在 `pages/<page>_page.py` 中声明定位器和高层动作（方法应只暴露业务行为，如 `login()`、`logout()`、`navigate_to_site()`）。
- 在 `core/base_page.py` 中提供 `find`/`click`/`type_text` 等工具，页面对象使用这些方法以保证等待和报错一致性。
- 测试用例示例（`tests/test_login.py`）：

```python
from web_ui_framework.pages.login_page import LoginPage

def test_login_success(browser, login_credentials):
	lp = LoginPage(browser)
	lp.open("https://example.com")
	lp.login_and_wait_for_home(login_credentials['username'], login_credentials['password'], "/#/homePage")
	assert "/#/homePage" in browser.current_url
```

 常见原则：
- 优先使用稳定定位（`id`、`data-test`、`name`），仅在必要时使用 XPath。 
- 把等待逻辑放到 `core` 或页面对象中，避免在测试中大量重复 `WebDriverWait`。
- 页面对象应返回业务信息（如 `widget_count()`），而不是暴露底层 WebDriver。

## 生成 HTML 报告

在本地或 CI 中可通过 `pytest-html` 生成 HTML 报告并保存到 `reports/html_reports/`：

```bash
pytest web_ui_framework --html=reports/html_reports/report.html --self-contained-html
```


## 其它注意事项

- `configs/settings.yaml` 中的 `chromedriver_path` 字段可用于在不同环境（`linux`/`windows`/`ci`）中指定驱动路径，框架会优先使用构造器或环境变量中的 `CHROMEDRIVER_PATH`。
- 在本地开发时，如果页面元素或定位器变化，优先更新 `pages/` 中的页面对象，而不是直接修改测试用例。
