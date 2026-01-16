# Web UI 自动化测试框架

这是一个基于 Selenium + pytest 的 Web UI 自动化测试框架示例脚手架。

目录结构与快速启动：

- 安装依赖：

```
python -m pip install -r requirements.txt
```

- 运行示例测试：

```
# 建议在仓库根运行，使用包导入路径：
pytest -q web_ui_framework
```

CI 配置
 - GitHub Actions: 已添加工作流文件 `.github/workflows/ci.yml`，会在推送或 PR 时运行 `pytest web_ui_framework` 并上传 HTML 报告。
 - Jenkins: 已添加顶级 `Jenkinsfile`，包含安装依赖与运行 `pytest web_ui_framework` 的阶段，并归档 HTML 报告。

在远程仓库启用 CI：
 - GitHub：推送到仓库并确保 `main` 或 `master` 分支存在，Actions 将自动触发。
 - Jenkins：在 Jenkins 中创建新的流水线任务并指向仓库，Jenkins 将使用 `Jenkinsfile`。
