# Cloudflare 部署指南 - watch-ricon-stock

## 通过 Cloudflare Pages 从 GitHub 导入部署

本项目可以轻松地从 GitHub 导入到 Cloudflare Pages，并通过环境变量配置进行部署。

### 部署步骤

1. **在 GitHub 创建仓库**
   - 将项目代码推送到 GitHub 仓库
   
2. **登录 Cloudflare Dashboard**
   - 访问 https://dash.cloudflare.com
   - 选择你的账户

3. **创建 Pages 项目**
   - 导航到 Pages 部分
   - 点击 "Create a project"
   - 选择 "Connect to Git"

4. **连接 GitHub 仓库**
   - 选择你的 watch-ricon-stock 仓库
   - 点击 "Begin setup"

5. **配置构建设置**
   - 构建输出目录: (留空)
   - 构建命令: `echo "Python app doesn't need build step"`
   - 环境变量: 见下文

6. **设置环境变量**
   在 Cloudflare Dashboard 中设置以下环境变量：
   
   - `SMTP_SERVER` - 邮件服务器 (如 smtp.gmail.com)
   - `SMTP_PORT` - 邮件服务器端口 (如 587) 
   - `SMTP_USER` - 邮箱账号
   - `SMTP_PASSWORD` - 邮箱密码或应用专用密码
   - `TO_EMAIL` - 接收通知的邮箱地址
   - `API_URL` - (可选) 监控的 API 地址
   - `POLLING_INTERVAL` - (可选) 轮询间隔（秒）

7. **部署项目**
   - 点击 "Save and Deploy"
   - Cloudflare Pages 将自动部署项目

### 配置说明

由于 Cloudflare Pages 主要用于托管静态网站，而这是一个 Python 应用，所以需要一些额外的配置：

1. **使用环境变量**：将敏感信息（邮箱账号密码）通过环境变量传递
2. **定时任务**：使用外部服务或 Cloudflare Cron Triggers 来定期运行监控脚本

### 部署后配置

项目部署后，您需要：

1. **使用环境变量创建配置文件**：
   程序会从环境变量读取配置，如果环境变量存在，将自动生成配置文件

2. **运行监控脚本**：
   - 由于 Pages 是静态托管，需要外部服务触发脚本执行
   - 可以使用 GitHub Actions、Cron Jobs 或其他服务器来定期运行

### 配置 Cloudflare Cron Triggers（可选）

为了实现自动监控，您可以配置 Cloudflare Cron Triggers：

1. 在 wrangler.toml 中添加:
```toml
[triggers]
crons = ["*/10 * * * *"]  # 每10分钟运行一次
```

2. 创建一个简单的触发端点来运行监控脚本

### 注意事项

1. **定时任务**：Cloudflare Pages 本身是静态托管，无法持续运行 Python 脚本
2. **外部触发**：需要外部服务定期触发监控脚本
3. **成本考虑**：如果需要持续监控，可能需要考虑 Cloudflare Workers Paid Plan 或其他服务器

### 简化部署方式

如果您只需要从 GitHub 导入并配置环境变量：

1. 在 Cloudflare Pages 项目设置中，添加环境变量
2. 项目会根据环境变量自动生成配置文件
3. 通过外部服务触发脚本执行