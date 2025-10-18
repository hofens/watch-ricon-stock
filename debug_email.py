import smtplib
import json
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("邮件配置测试工具")
print("="*50)

# 加载配置
with open('src/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

email_config = config.get('notification_config', {}).get('email', {})
smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
smtp_port = email_config.get('smtp_port', 587)
smtp_user = email_config.get('smtp_user', '')
smtp_password = email_config.get('smtp_password', '')
to_email = email_config.get('to_email', '')

print(f"SMTP服务器: {smtp_server}")
print(f"SMTP端口: {smtp_port}")
print(f"发件人邮箱: {smtp_user}")
print(f"收件人邮箱: {to_email}")

# 检查配置完整性
if not smtp_user or not smtp_password or not to_email:
    print("\n错误：配置不完整！")
    print("请检查以下配置项：")
    print("- smtp_user (邮件地址)")
    print("- smtp_password (密码或应用专用密码)")
    print("- to_email (收件人邮件地址)")
    exit()

print("\n正在测试邮件连接...")

try:
    # 尝试连接到SMTP服务器
    print(f"1. 正在连接到 {smtp_server}:{smtp_port}...")
    server = smtplib.SMTP(smtp_server, smtp_port)
    print("   连接成功！")

    # 启用TLS加密
    print("2. 启用TLS加密...")
    server.starttls()
    print("   TLS加密启用成功！")

    # 登录
    print("3. 尝试登录...")
    server.login(smtp_user, smtp_password)
    print("   登录成功！")

    # 发送测试邮件
    print("4. 发送测试邮件...")
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = "Product Monitor - 连接测试"
    
    body = "这是一个连接测试邮件，验证邮件配置是否正确。\n\n如果收到此邮件，说明邮件配置正常。"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    server.send_message(msg)
    print("   邮件发送成功！")

    server.quit()
    print("\n✓ 所有测试通过！邮件配置正常。")
    print("启动监控程序时应该会发送启动通知邮件。")

except smtplib.SMTPAuthenticationError as e:
    print(f"\n✗ 认证失败！请检查邮箱地址和密码：{e}")
    print("对于Gmail用户，请确保使用应用专用密码，而不是普通登录密码")
    print("对于QQ邮箱用户，请使用授权码而不是登录密码")

except smtplib.SMTPRecipientsRefused as e:
    print(f"\n✗ 收件人地址被拒绝：{e}")
    print("请检查收件人邮箱地址是否正确")

except smtplib.SMTPSenderRefused as e:
    print(f"\n✗ 发件人地址被拒绝：{e}")
    print("请检查发件人邮箱地址是否正确")

except (smtplib.SMTPConnectError, ConnectionRefusedError, ConnectionError) as e:
    print(f"\n✗ 连接错误：{e}")
    print("常见原因：")
    print("- SMTP服务器地址或端口错误")
    print("- 防火墙阻止连接")
    print("- 网络连接问题")
    print("- 服务商阻止了SMTP连接")
    
    # 提供常见服务商的正确设置
    print("\n常见服务商SMTP设置：")
    print("- Gmail: smtp.gmail.com:587")
    print("- QQ邮箱: smtp.qq.com:587")
    print("- 163邮箱: smtp.163.com:587")
    print("- Outlook: smtp-mail.outlook.com:587")

except Exception as e:
    print(f"\n✗ 未知错误：{e}")
    
    # 检查是否是SSL相关的错误，尝试SSL连接
    if "SSL" in str(e) or "tls" in str(e).lower():
        print("\n提示：如果是SSL/TLS相关错误，可以尝试使用SSL连接（端口465）")
        print("例如Gmail使用SMTP_SSL：")
        print("  server = smtplib.SMTP_SSL('smtp.gmail.com', 465)")

print("\n" + "="*50)
print("测试完成")