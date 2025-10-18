#!/bin/bash
# Cloudflare Pages 部署准备脚本

echo "准备部署 watch-ricon-stock 到 Cloudflare Pages..."

echo "步骤 1: 检查项目依赖"
if ! command -v git &> /dev/null; then
    echo "错误: Git 未安装或不可用"
    exit 1
fi

echo "步骤 2: 确保代码已提交"
git_status=$(git status --porcelain)
if [[ -n "$git_status" ]]; then
    echo "警告: 工作目录有未提交的更改，建议先提交"
    read -p "是否继续? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "步骤 3: 验证配置"
echo "在 Cloudflare Pages 部署时，请设置以下环境变量:"
echo "  - SMTP_SERVER: 邮件服务器 (如 smtp.gmail.com)"
echo "  - SMTP_PORT: 邮件服务器端口 (如 587)"
echo "  - SMTP_USER: 邮箱账号"
echo "  - SMTP_PASSWORD: 邮箱密码或应用专用密码" 
echo "  - TO_EMAIL: 接收通知的邮箱地址"
echo "  - API_URL: (可选) 监控的 API 地址"
echo "  - POLLING_INTERVAL: (可选) 轮询间隔（秒）"

echo
echo "步骤 4: 部署到 Cloudflare Pages"
echo "1. 访问 https://dash.cloudflare.com"
echo "2. 导航到 Pages 部分"
echo "3. 点击 'Create a project' -> 'Connect to Git'"
echo "4. 选择您的 watch-ricon-stock 仓库"
echo "5. 在 'Environment Variables' 部分添加上述变量"
echo "6. 点击 'Save and Deploy'"

echo
echo "注意: Cloudflare Pages 本身不会持续运行 Python 脚本。"
echo "要实现监控功能，您需要:"
echo "- 使用外部服务定时触发 /start 端点"
echo "- 或使用 GitHub Actions 定时运行监控脚本"

echo "部署准备完成！"