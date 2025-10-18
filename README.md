# watch-ricon-stock - Ricn Mall Stock Monitor

watch-ricon-stock is a powerful monitoring tool that tracks product listing changes and stock updates on the Ricn Mall API and provides comprehensive notifications when changes occur.

## Features

- Monitors the Ricn Mall API at regular intervals
- Detects new, removed, and updated products with detailed information
- Tracks stock level changes in real-time
- Supports multiple notification methods (console, file, email)
- Configurable polling interval
- Time range restriction (monitor only during specified hours)
- Detailed change logs with full product information
- Startup notifications with current product listings
- Comprehensive email notifications with detailed product changes

## Requirements

- Python 3.6 or higher
- Required Python packages (see requirements.txt)

## Installation

1. Clone or download this repository
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration

The program uses a `config.json` file for configuration:

```json
{
    "api_url": "https://newsite.ricn-mall.com/api/pc/get_products?page=1&limit=10&cid=9&sid=0&priceOrder=&news=0",
    "polling_interval_seconds": 300,
    "notification_method": "console",
    "notification_config": {
        "email": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "smtp_user": "your_email@gmail.com",
            "smtp_password": "your_app_password",
            "to_email": "recipient@example.com"
        }
    },
    "time_range": {
        "enable": false,
        "start_time": "09:00",
        "end_time": "23:59"
    },
    "log_file": "product_monitor.log",
    "changes_log": "product_changes.log"
}
```

### Configuration Options

- `api_url`: The API endpoint to monitor (default: Ricn Mall products API)
- `polling_interval_seconds`: Time between API requests in seconds (default: 300 = 5 minutes)
- `notification_method`: How to receive notifications (`console`, `file`, or `email`)
- `time_range`: Time range configuration for monitoring (optional)
  - `enable`: Whether to enable time range restriction (default: false)
  - `start_time`: Start time in HH:MM format (default: "09:00")
  - `end_time`: End time in HH:MM format (default: "23:59")
- `notification_config`: Email configuration when using email notifications
  - `email`: Email server settings
    - `smtp_server`: SMTP server address
    - `smtp_port`: SMTP server port
    - `smtp_user`: SMTP username (your email address)
    - `smtp_password`: SMTP password (app-specific password for Gmail)
    - `to_email`: Recipient email address
- `log_file`: Path to the main application log file
- `changes_log`: Path to the changes log file (used when notification method is 'file')

### Email Configuration

To use email notifications, set `notification_method` to `email` and configure the SMTP settings in `notification_config.email`.

## Usage

Run the monitor with the default configuration:

```bash
python src/product_monitor.py
```

Or specify a custom configuration file:

```bash
python src/product_monitor.py --config /path/to/your/config.json
```

## Notification Methods

1. **Console**: Print changes to standard output
2. **File**: Write changes to the specified changes log file
3. **Email**: Send an email notification (requires proper email configuration)

## Stopping the Monitor

Press `Ctrl+C` to stop the monitoring process.

## Logs

- `product_monitor.log`: Contains application logs
- `product_changes.log`: Contains change notifications (when using 'file' notification method)

## Setup and Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Step-by-step Setup

1. **Clone or download the project**
   ```bash
   git clone <repository-url>  # if using git
   # or download and extract the zip file
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**
   - Edit `src/config.json` with your specific settings
   - Set your API endpoint, polling interval, and notification preferences

4. **Set up email notifications (optional)**
   - Configure your email provider settings in `src/config.json`
   - For Gmail: Enable 2FA and generate an App Password
   - For other providers: Enable IMAP/SMTP and get the authorization code

5. **Run the application**
   - Use the provided batch file: `start_monitor.bat`
   - Or run directly: `python src/product_monitor.py`

## Configuration Examples

### Basic Configuration (Console Notifications)
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

### Email Notification Configuration
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

## Email Configuration Guide

### Gmail Setup
1. Enable 2-Step Verification in your Google Account
2. Go to Security settings
3. Under "Signing in to Google," select "App passwords"
4. Generate a new app password for "Mail"
5. Use this 16-character password as `smtp_password`

### QQ Mail Setup
1. Log into QQ Mail web interface
2. Go to Settings → Account
3. Enable "IMAP/SMTP Service"
4. Generate authorization code
5. Use authorization code as `smtp_password`

### Other Providers
- Most email providers require enabling IMAP/SMTP
- Use the provider's SMTP server and port
- Use authorization code instead of login password

## Usage Scenarios

### Scenario 1: Continuous Monitoring
- Set `time_range.enable: false`
- Program will monitor 24/7

### Scenario 2: Business Hours Monitoring  
- Set `time_range.enable: true`
- Configure `start_time` and `end_time`
- Program will only operate during specified hours

### Scenario 3: Debugging
- Set `notification_method: "console"`
- View changes directly in command line

## Troubleshooting

### Common Issues

**Issue**: Email authentication failed
- **Solution**: Ensure you're using app password, not regular login password
- Verify SMTP settings match your email provider

**Issue**: Can't connect to SMTP server  
- **Solution**: Check firewall settings, verify SMTP server and port
- Try different ports (587 vs 465 vs 25)

**Issue**: Program runs but no notifications
- **Solution**: Check notification_method setting, verify configuration file path
- Review log files for error messages

**Issue**: False change detections
- **Solution**: This is normal behavior - program establishes baseline on first run

### Log Files
- Check `product_monitor.log` for application errors
- Check `product_changes.log` for notification logs (when using file method)

## Running the Application

### Method 1: Using Batch File
1. Double-click `start_monitor.bat`
2. The application will run with default configuration

### Method 2: Command Line
```bash
# Run with default config
python src/product_monitor.py

# Run with custom config
python src/product_monitor.py --config path/to/your/config.json
```

### Keeping the Application Running
- Use a Windows service manager to run continuously
- Or use task scheduling for periodic restarts
- Monitor log files to ensure continued operation

## Project Structure
```
watch-ricon-stock/
├── src/
│   ├── product_monitor.py    # Main monitoring application
│   └── config.json          # Default configuration
├── start_monitor.bat        # Windows startup script
├── requirements.txt         # Python dependencies
├── README.md              # This file
├── product_monitor.log    # Application logs (generated)
└── product_changes.log    # Change notifications (generated)
```

## License
This project is open source and available under the MIT License.

---

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

使用默认配置运行监控器：

```bash
python src/product_monitor.py
```

或指定自定义配置文件：

```bash
python src/product_monitor.py --config /path/to/your/config.json
```

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
├── README.md              # 本文件
├── product_monitor.log    # 应用程序日志（生成的）
└── product_changes.log    # 变更通知（生成的）
```

## 许可证
本项目开源，采用 MIT 许可证。