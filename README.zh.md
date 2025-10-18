# watch-ricon-stock - Ricn Mall 库存监控器

watch-ricon-stock 是一个功能强大的监控工具，用于跟踪 Ricn Mall API 上的商品列表变化和库存更新，并在发生变更时提供全面的通知。

## 功能特性

- 定期监控 Ricn Mall API
- 检测新增、删除和更新的商品，并提供详细信息
- 实时跟踪库存水平变化
- 支持多种通知方式（控制台、文件、邮件）
- 可配置的轮询间隔
- 时间范围限制（仅在指定时间内监控）
- 包含完整商品信息的详细日志
- 启动时通知包含当前商品列表
- 包含详细商品变更的综合邮件通知

## 要求

- Python 3.6 或更高版本
- 需要 Python 包（见 requirements.txt）

## 安装

1. 克隆或下载此仓库
2. 安装所需 Python 包：

```bash
pip install -r requirements.txt
```

## 配置

程序使用 `config.json` 文件进行配置：

```json
{
    "api_url": "https://newsite.ricn-mall.com/api/pc/get_products?page=1&limit=10&cid=9&sid=0&priceOrder=&news=0",
    "polling_interval_seconds": 300,
    "notification_method": "console",
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

### 配置选项

- `api_url`: 要监控的 API 端点（默认：Ricn Mall 商品 API）
- `polling_interval_seconds`: API 请求间隔时间（秒）（默认：300 = 5 分钟）
- `notification_method`: 接收通知的方式（`console`、`file` 或 `email`）
- `time_range`: 监控的时间范围配置（可选）
  - `enable`: 是否启用时间范围限制（默认：false）
  - `start_time`: 开始时间，格式 HH:MM（默认："09:00"）
  - `end_time`: 结束时间，格式 HH:MM（默认："23:59"）
- `notification_config`: 邮件通知的配置
  - `email`: 邮件服务器设置
    - `smtp_server`: SMTP 服务器地址
    - `smtp_port`: SMTP 服务器端口
    - `smtp_user`: SMTP 用户名（邮箱地址）
    - `smtp_password`: SMTP 密码（Gmail 的应用专用密码）
    - `to_email`: 收件人邮箱地址
- `log_file`: 主应用程序日志文件路径
- `changes_log`: 变更日志文件路径（当通知方式为 'file' 时使用）

### 邮件配置

要使用邮件通知，将 `notification_method` 设置为 `email` 并在 `notification_config.email` 中配置 SMTP 设置。

## 使用方法

使用自动配置检测运行监控器（按顺序检查：config.local.json, config.json）：

```bash
python src/product_monitor.py
```

或指定自定义配置文件：

```bash
python src/product_monitor.py --config /path/to/your/config.json
```

### 配置文件优先级
程序将按以下优先级顺序查找配置文件：
1. 命令行参数（如果提供了 `--config`）
2. `src/config.local.json`（用于本地配置 - 这是推荐方法）
3. `config.local.json`（在当前目录中）
4. `src/config.json`（默认配置）
5. `config.json`（在当前目录中）

这个系统允许您创建 `config.local.json` 文件来保存个人设置，这些设置不会被提交到版本控制中，因为 `config.local.json` 已包含在 `.gitignore` 中。

## 通知方式

1. **控制台**: 在标准输出打印变更
2. **文件**: 写入指定的变更日志文件
3. **邮件**: 发送邮件通知（需要正确的邮件配置）

## 停止监控

按 `Ctrl+C` 停止监控进程。

## 日志

- `product_monitor.log`: 包含应用程序日志
- `product_changes.log`: 包含变更通知（当使用 'file' 通知方式时）

## 安装和配置指南

### 前置要求
- Python 3.6 或更高版本
- pip 包管理器

### 分步设置

1. **克隆或下载项目**
   ```bash
   git clone <repository-url>  # 如果使用 git
   # 或下载并解压 zip 文件
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置应用程序**
   - 编辑 `src/config.json` 以设置特定配置
   - 设置 API 端点、轮询间隔和通知首选项

4. **设置邮件通知（可选）**
   - 在 `src/config.json` 中配置邮箱提供商设置
   - 对于 Gmail：启用两步验证并生成应用密码
   - 对于其他提供商：启用 IMAP/SMTP 并获取授权码

5. **运行应用程序**
   - 使用提供的批处理文件：`start_monitor.bat`
   - 或直接运行：`python src/product_monitor.py`

## 配置示例

### 基础配置（控制台通知）
```json
{
    "api_url": "https://newsite.ricn-mall.com/api/pc/get_products?page=1&limit=10&cid=9&sid=0&priceOrder=&news=0",
    "polling_interval_seconds": 300,
    "notification_method": "console",
    "time_range": {
        "enable": false
    },
    "log_file": "product_monitor.log",
    "changes_log": "product_changes.log"
}
```

### 邮件通知配置
```json
{
    "api_url": "https://newsite.ricn-mall.com/api/pc/get_products?page=1&limit=10&cid=9&sid=0&priceOrder=&news=0",
    "polling_interval_seconds": 300,
    "notification_method": "email",
    "time_range": {
        "enable": true,
        "start_time": "09:00",
        "end_time": "23:00"
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

## 邮件配置指南

### Gmail 设置
1. 在 Google 账户中启用两步验证
2. 进入安全设置
3. 在"登录到 Google"下，选择"应用密码"
4. 为"邮件"生成新的应用密码
5. 使用此 16 位字符密码作为 `smtp_password`

### QQ 邮箱设置
1. 登录 QQ 邮箱网页版
2. 进入设置 → 账户
3. 启用"IMAP/SMTP 服务"
4. 生成授权码
5. 使用授权码作为 `smtp_password`

### 其他提供商
- 大多数邮箱提供商需要启用 IMAP/SMTP
- 使用提供商的 SMTP 服务器和端口
- 使用授权码而不是登录密码

## 使用场景

### 场景 1：连续监控
- 设置 `time_range.enable: false`
- 程序将 24/7 监控

### 场景 2：工作时间监控
- 设置 `time_range.enable: true`
- 配置 `start_time` 和 `end_time`
- 程序只在指定时间内运行

### 场景 3：调试
- 设置 `notification_method: "console"`
- 在命令行直接查看变更

## 故障排除

### 常见问题

**问题**: 邮箱认证失败
- **解决方案**: 确保您使用的是应用密码，而不是常规登录密码
- 验证 SMTP 设置是否匹配您的邮箱提供商

**问题**: 无法连接到 SMTP 服务器
- **解决方案**: 检查防火墙设置，验证 SMTP 服务器和端口
- 尝试不同端口（587、465 或 25）

**问题**: 程序运行但没有通知
- **解决方案**: 检查 notification_method 设置，验证配置文件路径
- 查看日志文件中的错误消息

**问题**: 错误的变更检测
- **解决方案**: 这是正常行为 - 程序在第一次运行时建立基线

### 日志文件
- 查看 `product_monitor.log` 获取应用程序错误
- 查看 `product_changes.log` 获取通知日志（当使用文件方式时）

## 运行应用程序

### 方法 1：使用批处理文件
1. 双击 `start_monitor.bat`
2. 应用程序将使用默认配置运行

### 方法 2：命令行
```bash
# 使用默认配置运行
python src/product_monitor.py

# 使用自定义配置运行
python src/product_monitor.py --config path/to/your/config.json
```

### 保持应用程序运行
- 使用 Windows 服务管理器持续运行
- 或使用任务计划程序进行定期重启
- 监控日志文件以确保持续运行

## 项目结构
```
watch-ricon-stock/
├── src/
│   ├── product_monitor.py    # 主监控应用程序
│   └── config.json          # 默认配置
├── start_monitor.bat        # Windows 启动脚本
├── requirements.txt         # Python 依赖
├── README.md              # 英文文档
├── README.zh.md           # 中文文档
├── product_monitor.log    # 应用程序日志（生成的）
└── product_changes.log    # 变更通知（生成的）
```

## Cloudflare 部署

本项目包含对 Cloudflare 基础设施部署的支持，使用 Python Workers。详情请参阅 `CLOUDFLARE_DEPLOY.md` 了解如何部署应用程序。项目现在支持：

- Cloudflare Python Workers（需要 python_workers 兼容性标志）
- 环境变量配置敏感数据
- 基于 Flask 的 Web API 用于 HTTP 访问
- 从环境变量自动生成配置

项目包含：
- 基于 Flask 的 Web API（`web_api.py`）用于 HTTP 访问
- 用于 Cloudflare Workers 的 Wrangler 配置
- 从环境变量生成配置
- 用于设置辅助的部署脚本

**注意**：Cloudflare Python Workers 支持可能需要特殊访问权限或处于测试阶段。请查看 Cloudflare 文档了解当前可用性。

## 许可证
本项目开源，采用 MIT 许可证。