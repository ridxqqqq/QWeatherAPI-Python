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
| `.github/workflows/python-app.yml` | GitHub Actions 定时任务（每天 07:00）与手动触发 |

`myKey.py` 已被 `.gitignore` 排除，请勿将真实密钥提交到仓库。

## 定时推送与企业微信通知

工作流已配置为**每天 07:00（Asia/Shanghai）自动运行**，并将天气摘要推送到企业微信群。

配置步骤：

1. 在企业微信目标群的「群设置 → 群机器人」中添加机器人，复制 Webhook 地址（形如 `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...`）
2. 在仓库 **Settings → Secrets and variables → Actions** 中添加：

   | Secret | 说明 |
   |--------|------|
   | `QWEATHER_KEY` | 和风天气 API KEY |
   | `QWEATHER_HOST` | 和风天气 API Host |
   | `QWEATHER_WECHAT_WEBHOOK` | 企业微信群机器人 Webhook 地址 |

3. 在 **Actions** 页面手动触发一次 `Python CI_test` 验证；之后每天会自动执行

说明：

- GitHub Actions 的 cron 使用 **UTC** 时间，`0 23 * * *` 对应北京时间次日 07:00
- 定时任务只会运行默认分支（`main`）上的工作流，请确保改动已合并到 `main`
- GitHub 的定时触发可能有几分钟到一小时的延迟
- 本地运行时若未设置 `QWEATHER_WECHAT_WEBHOOK` 环境变量，只打印天气、不发送通知

