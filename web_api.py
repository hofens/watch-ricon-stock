"""
watch-ricon-stock Web API Interface
为Cloudflare部署创建一个简单的Web API接口
"""
from flask import Flask, jsonify, request
import os
import threading
import time
from src.product_monitor import ProductMonitor

app = Flask(__name__)

# 全局监控器实例
monitor = None
monitor_thread = None
is_monitoring = False

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
            "/products"
        ]
    })

@app.route('/start', methods=['POST'])
def start_monitor():
    global monitor, monitor_thread, is_monitoring
    
    if is_monitoring:
        return jsonify({"message": "Monitor is already running"}), 400
    
    try:
        config_file = request.json.get('config', 'src/config.local.json') if os.path.exists('src/config.local.json') else 'src/config.json'
        
        # 创建监控器
        monitor = ProductMonitor(config_file=config_file)
        
        # 启动监控线程
        def run_monitor():
            global is_monitoring
            is_monitoring = True
            monitor.start_monitoring()
        
        monitor_thread = threading.Thread(target=run_monitor, daemon=True)
        monitor_thread.start()
        
        return jsonify({"message": "Monitor started successfully"})
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
        "monitoring": is_monitoring
    })

@app.route('/products', methods=['GET'])
def get_products():
    try:
        # 这里可以添加获取最新产品数据的功能
        # 注意：实际产品监控需要在后台运行
        return jsonify({
            "message": "Product monitoring is running in background",
            "status": "active" if is_monitoring else "inactive"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)