# GitHub Actions 部署指南 - watch-ricon-stock

通过 GitHub Actions 可以实现自动部署和运行 watch-ricon-stock 监控程序。

## 设置步骤

### 1. 创建 GitHub 仓库
- 将项目代码推送到 GitHub 仓库

### 2. 配置仓库 Secrets
在 GitHub 仓库中设置以下 Secrets（Settings > Secrets and variables > Actions）：

必需的 Secrets：
- `SMTP_SERVER` - 邮件服务器（如 smtp.gmail.com）
- `SMTP_PORT` - 邮件服务器端口（如 587）
- `SMTP_USER` - 邮箱账号
- `SMTP_PASSWORD` - 邮件应用密码
- `TO_EMAIL` - 接收通知的邮箱地址

可选的 Secrets：
- `API_URL` - 监控的 API 地址 (默认: Ricn Mall 产品 API)
- `POLLING_INTERVAL` - 轮询间隔（秒）(默认: 300)
- `NOTIFICATION_METHOD` - 通知方式 (默认: email)
- `TIME_RANGE_ENABLE` - 是否启用时间段 (默认: false)
- `START_TIME` - 开始时间 (默认: 09:00)
- `END_TIME` - 结束时间 (默认: 23:59)

### 3. 工作流配置说明

当前的工作流配置：
- 每10分钟自动运行一次监控程序
- 也可以通过手动触发运行
- 从 GitHub Secrets 生成配置文件
- 运行监控程序检测产品变化

### 4. 自定义运行频率

修改 `.github/workflows/deploy.yml` 中的 cron 表达式来调整运行频率：

```yaml
schedule:
  - cron: '*/10 * * * *'  # 每10分钟
```

Cron 表达式格式：`分钟 小时 日 月 星期`

示例：
- 每5分钟: `*/5 * * * *`
- 每小时: `0 * * * *`
- 每天上午9点: `0 9 * * *`

### 5. 查看运行日志

- 在 Actions 标签页中查看工作流运行状态
- 点击具体的运行查看详细日志
- 如果监控程序检测到产品变化，日志中会显示详细信息

### 6. 故障排除

- 检查 Secrets 是否正确配置
- 确认邮箱配置是否正确（使用应用密码而非登录密码）
- 查看 Actions 日志中的错误信息

## 注意事项

- GitHub Actions 的运行时间有限制，适合定时检查而非持续监控
- 由于免费账户的限制，请合理设置运行频率
- 邮件通知功能需要正确配置邮箱服务