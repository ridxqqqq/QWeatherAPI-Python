# <img src="https://cdn.qweather.com/media/logo-dark-30.png" width="30" height="30" alt="数据来自和风天气" />  QWeatherAPI-Python  <img src="https://cdn.qweather.com/media/powered-by-heweather-dark2.png"  width="160" height="20" alt="数据来自和风天气" />
![GitHub Repo stars](https://img.shields.io/github/stars/InTereSTingHE/QWeatherAPI-Python?style=social)

使用 Python 的 requests 库实现和风天气 API 调用。

## 快速开始

1. 登录[和风天气控制台](https://console.qweather.com)创建项目与 API KEY，并在「设置」中查看你的 API Host
2. 复制凭据模板并填写：

   ```bash
   cp myKey.example.py myKey.py
   ```

   ```python
   KEY = '你的 API KEY'
   API_HOST = '你的 API Host'
   ```

3. 安装依赖并运行：

   ```bash
   pip install requests
   python QWeatherAPI.py
   ```

## 目录说明

| 文件 | 说明 |
|------|------|
| `QWeatherAPI.py` | 天气 API 调用示例（实况 / 逐日 / 逐小时 / 分钟级降水 / 空气质量） |
| `myKey.example.py` | 凭据配置模板，复制为 `myKey.py` 后填写 |
| `.github/workflows/python-app.yml` | GitHub Actions 手动触发的运行检查 |

`myKey.py` 已被 `.gitignore` 排除，请勿将真实密钥提交到仓库。

## 在 GitHub Actions 中运行

在仓库 **Settings → Secrets and variables → Actions** 中添加：

- `QWEATHER_KEY`：你的 API KEY
- `QWEATHER_HOST`：你的 API Host

然后在 **Actions** 页面手动触发 `Python CI_test` 工作流即可。
