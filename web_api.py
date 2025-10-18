"""
watch-ricon-stock Web API Interface
为Cloudflare部署创建一个简单的Web API接口
"""
from flask import Flask, jsonify, request
import os
import json
import threading
from src.product_monitor import ProductMonitor

app = Flask(__name__)

# 全局监控器实例
monitor = None
monitor_thread = None
is_monitoring = False

def create_config_from_env():
    """从环境变量创建配置文件"""
    config = {
        "api_url": os.environ.get('API_URL', 'https://newsite.ricn-mall.com/api/pc/get_products?page=1&limit=10&cid=9&sid=0&priceOrder=&news=0'),
        "polling_interval_seconds": int(os.environ.get('POLLING_INTERVAL', 300)),
        "notification_method": "email",
        "time_range": {
            "enable": False,
            "start_time": "09:00",
            "end_time": "23:59"
        },
        "notification_config": {
            "email": {
                "smtp_server": os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
                "smtp_port": int(os.environ.get('SMTP_PORT', 587)),
                "smtp_user": os.environ.get('SMTP_USER', ''),
                "smtp_password": os.environ.get('SMTP_PASSWORD', ''),
                "to_email": os.environ.get('TO_EMAIL', '')
            }
        },
        "log_file": "product_monitor.log",
        "changes_log": "product_changes.log"
    }
    
    # 保存到临时配置文件
    config_path = 'src/config.cf.json'
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    return config_path

@app.route('/')
def home():
    return jsonify({
        "message": "watch-ricon-stock API is running",
        "status": "active" if is_monitoring else "inactive",
        "endpoints": [
            "/",
            "/start",
            "/stop", 
            "/status",
            "/products",
            "/health"
        ]
    })

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点，适合Cloudflare使用"""
    return jsonify({
        "status": "healthy",
        "service": "watch-ricon-stock",
        "timestamp": os.environ.get('CURRENT_TIMESTAMP', '')
    })

@app.route('/start', methods=['POST'])
def start_monitor():
    global monitor, monitor_thread, is_monitoring
    
    if is_monitoring:
        return jsonify({"message": "Monitor is already running"}), 400
    
    try:
        # 从环境变量创建配置文件
        config_path = create_config_from_env()
        
        # 创建监控器
        monitor = ProductMonitor(config_file=config_path)
        
        # 启动监控线程
        def run_monitor():
            global is_monitoring
            is_monitoring = True
            monitor.start_monitoring()
        
        monitor_thread = threading.Thread(target=run_monitor, daemon=True)
        monitor_thread.start()
        
        return jsonify({
            "message": "Monitor started successfully",
            "config_source": "environment_variables"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop_monitor():
    global is_monitoring
    if not is_monitoring:
        return jsonify({"message": "Monitor is not running"}), 400
    
    is_monitoring = False
    return jsonify({"message": "Monitor stopped"})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "active" if is_monitoring else "inactive",
        "monitoring": is_monitoring,
        "config_source": "environment_variables" if os.environ.get('SMTP_USER') else "default_file"
    })

@app.route('/products', methods=['GET'])
def get_products():
    try:
        # 这里可以添加获取最新产品数据的功能
        # 注意：实际产品监控需要在后台运行
        return jsonify({
            "message": "Product monitoring is running in background",
            "status": "active" if is_monitoring else "inactive",
            "config_source": "environment_variables" if os.environ.get('SMTP_USER') else "default_file"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)