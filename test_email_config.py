import sys
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 添加项目源码路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 从配置文件加载配置
with open('src/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

print(f"配置文件加载成功")
print(f"通知方式: {config.get('notification_method')}")
print(f"API URL: {config.get('api_url')}")
print(f"轮询间隔: {config.get('polling_interval_seconds')} 秒")

# 检查是否配置了邮件
if config.get('notification_method') == 'email':
    email_config = config.get('notification_config', {}).get('email', {})
    print(f"SMTP 服务器: {email_config.get('smtp_server')}")
    print(f"SMTP 端口: {email_config.get('smtp_port')}")
    print(f"SMTP 用户: {email_config.get('smtp_user')}")
    print(f"收件邮箱: {email_config.get('to_email')}")
    
    # 尝试发送测试邮件
    try:
        smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = email_config.get('smtp_port', 587)
        smtp_user = email_config.get('smtp_user', '')
        smtp_password = email_config.get('smtp_password', '')
        to_email = email_config.get('to_email', '')
        
        if not smtp_user or not smtp_password or not to_email:
            print("错误：邮件配置不完整，请检查配置文件中的以下字段：")
            print("- smtp_user (邮箱地址)")
            print("- smtp_password (邮箱密码或应用专用密码)")
            print("- to_email (收件人邮箱)")
        else:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = to_email
            msg['Subject'] = "Product Monitor - 测试邮件"
            
            body = "这是一封测试邮件，确认邮件配置正常工作。\n\nProduct Monitor 启动测试邮件发送成功！"
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 尝试发送邮件
            print("正在尝试发送测试邮件...")
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            server.quit()
            
            print(f"测试邮件已成功发送到 {to_email}")
            
    except Exception as e:
        print(f"发送邮件失败: {e}")
        print("常见问题：")
        print("1. 邮箱密码错误或不是应用专用密码")
        print("2. SMTP服务器或端口配置错误")
        print("3. 网络连接问题")
        print("4. 邮箱安全设置阻止了SMTP登录")
else:
    print("当前配置的通知方式不是邮件，请检查 config.json 中的 notification_method 设置")
    print("请确保设置为: \"email\"")