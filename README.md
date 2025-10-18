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