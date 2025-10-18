# Cloudflare 部署指南 - watch-ricon-stock

## 通过 Cloudflare Workers 部署 Python 应用

本项目支持通过 Cloudflare Workers 部署 Python 应用，并通过环境变量配置进行部署。

### 前提条件

- Cloudflare 的 Python Workers 功能需要在 Beta 阶段进行申请或使用支持的账户
- 需要 `python_workers` 兼容性标志

### 部署步骤

1. **在 GitHub 创建仓库**
   - 将项目代码推送到 GitHub 仓库
   
2. **安装 Wrangler CLI**
   ```bash
   npm install -g wrangler
   ```

3. **登录 Cloudflare**
   ```bash
   wrangler login
   ```

4. **部署项目**
   ```bash
   wrangler deploy
   ```

5. **设置环境变量**
   在 wrangler.toml 中或通过 Cloudflare Dashboard 设置以下环境变量：
   
   - `SMTP_SERVER` - 邮件服务器 (如 smtp.gmail.com)
   - `SMTP_PORT` - 邮件服务器端口 (如 587) 
   - `SMTP_USER` - 邮箱账号
   - `SMTP_PASSWORD` - 邮箱密码或应用专用密码
   - `TO_EMAIL` - 接收通知的邮箱地址
   - `API_URL` - (可选) 监控的 API 地址
   - `POLLING_INTERVAL` - (可选) 轮询间隔（秒）

### 配置说明

1. **wrangler.toml 配置**:
   ```toml
   name = "watch-ricon-stock"
   compatibility_date = "2024-10-18"
   compatibility_flags = ["python_workers"]
   ```

2. **环境变量**: 敏感信息（邮箱账号密码）通过环境变量传递

### 部署后配置

1. **使用环境变量创建配置文件**：
   Web API 会从环境变量读取配置并自动生成配置文件

2. **运行监控脚本**：
   - 通过 HTTP 请求触发 `/start` 端点启动监控
   - 使用 Cloudflare Cron Triggers 实现定时监控

### 配置 Cloudflare Cron Triggers

为了实现自动监控，您可以配置 Cron Triggers：

在 wrangler.toml 中添加:
```toml
[triggers]
crons = ["*/10 * * * *"]  # 每10分钟运行一次
```

### 注意事项

1. **Python Workers 支持**: 这需要 Cloudflare 的 Python Workers 支持
2. **兼容性标志**: 需要 `python_workers` 兼容性标志
3. **持续监控**: 可以使用 Cron Triggers 实现定时检查

### 环境变量配置方式

在 Cloudflare Dashboard 中:
1. 进入 Workers & Pages
2. 选择你的 worker
3. 点击 "Settings" -> "Environment Variables"
4. 添加所需的环境变量

或者在 wrangler.toml 中配置:
```toml
[vars]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USER = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"
TO_EMAIL = "recipient@example.com"
API_URL = "https://newsite.ricn-mall.com/api/pc/get_products?page=1&limit=10&cid=9&sid=0&priceOrder=&news=0"
POLLING_INTERVAL = "300"
```