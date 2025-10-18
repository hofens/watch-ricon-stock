# Cloudflare 部署指南 - watch-ricon-stock

## 部署选项

本项目提供了多种在 Cloudflare 平台上部署的选项：

### 选项 1: Cloudflare Workers with Workers KV (推荐)
适用于轻量级部署和调度任务。

### 选项 2: Cloudflare Pages + Functions
适用于需要更复杂后端逻辑的部署。

### 选项 3: Cloudflare Container (Docker)
适用于完整的容器化部署。

## 选项 3: Docker 部署 (适用于 Cloudflare Container)

### 部署步骤:

1. **准备 Docker 镜像**
   ```bash
   docker build -t watch-ricon-stock .
   ```

2. **运行容器本地测试**
   ```bash
   docker run -p 5000:5000 watch-ricon-stock
   ```

3. **将镜像推送到容器注册表**
   ```bash
   # 登录到容器注册表（如 Docker Hub 或 Cloudflare Registry）
   docker tag watch-ricon-stock <your_registry>/watch-ricon-stock:latest
   docker push <your_registry>/watch-ricon-stock:latest
   ```

4. **在 Cloudflare 部署**
   - 访问 Cloudflare Dashboard
   - 进入 Workers & Pages
   - 选择 "Create a project" -> "Deploy a container image"
   - 输入你的镜像地址

## 配置

### 环境变量
容器需要以下环境变量：

- `CONFIG_FILE` - 配置文件路径 (默认: `src/config.json`)

### 挂载配置卷
推荐将配置文件挂载到容器中：
```bash
docker run -p 5000:5000 -v /path/to/config:/app/src/config.json watch-ricon-stock
```

## API 端点

应用提供了以下 REST API 端点:
- `GET /` - 获取应用状态
- `POST /start` - 启动监控
- `POST /stop` - 停止监控  
- `GET /status` - 获取监控状态
- `GET /products` - 获取产品状态

## Web API 功能

Web API 将原命令行监控器包装为 HTTP 服务，支持:
- 远程启动/停止监控
- 实时状态检查
- 与 Cloudflare 的无缝集成

## 注意事项

1. **持续运行**: 由于这是监控应用，需要保持持续运行
2. **调度**: 你可以使用外部服务（如 CRON）来定期触发 API
3. **健康检查**: `/` 和 `/status` 端点可以作为健康检查
4. **日志**: 日志输出到标准输出，Cloudflare 会自动收集

## 环境配置

创建一个 config.local.json 文件放在容器的 /app/src/ 盕录下：

```json
{
  "api_url": "https://newsite.ricn-mall.com/api/pc/get_products?page=1&limit=10&cid=9&sid=0&priceOrder=&news=0",
  "polling_interval_seconds": 300,
  "notification_method": "email",
  "time_range": {
    "enable": false,
    "start_time": "09:00",
    "end_time": "23:59"
  },
  "notification_config": {
    "email": {
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "smtp_user": "your_email@gmail.com",
      "smtp_password": "your_app_password",
      "to_email": "recipient@example.com"
    }
  },
  "log_file": "product_monitor.log",
  "changes_log": "product_changes.log"
}
```

## 部署到 Cloudflare 的优点

- 全球 CDN 分发
- 内置 DDoS 保护
- 可靠的基础设施
- 与 Cloudflare 生态系统集成