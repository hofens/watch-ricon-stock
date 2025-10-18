#!/bin/bash
# Cloudflare 部署脚本

echo "准备部署 watch-ricon-stock 到 Cloudflare..."

echo "重要提醒: Cloudflare Python Workers 目前可能处于 Beta 阶段"
echo "如果没有 Python Workers 访问权限，请考虑使用 Docker 部署方案"

echo
echo "选项 1: Python Workers 部署 (需要特殊访问权限)"
echo "------------------------"

echo "步骤 1: 检查必要工具"
if ! command -v npm &> /dev/null; then
    echo "错误: npm 未安装或不可用"
    exit 1
fi

if ! command -v wrangler &> /dev/null; then
    echo "Wrangler 未安装，正在安装..."
    npm install -g wrangler
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

echo "步骤 3: 登录 Cloudflare"
echo "运行 'wrangler login' 并按照提示登录"
echo "注意: Python Workers 可能需要 Beta 访问权限"

echo "步骤 4: 验证配置"
echo "部署前，请确保已在 wrangler.toml 或 Cloudflare Dashboard 中设置以下环境变量:"
echo "  - SMTP_SERVER: 邮件服务器 (如 smtp.gmail.com)"
echo "  - SMTP_PORT: 邮件服务器端口 (如 587)"
echo "  - SMTP_USER: 邮箱账号"
echo "  - SMTP_PASSWORD: 邮箱密码或应用专用密码" 
echo "  - TO_EMAIL: 接收通知的邮箱地址"
echo "  - API_URL: (可选) 监控的 API 地址"
echo "  - POLLING_INTERVAL: (可选) 轮询间隔（秒）"

echo
echo "步骤 5: 部署到 Cloudflare Workers"
echo "运行部署命令:"
echo "  wrangler deploy"

echo
echo "选项 2: Docker 部署 (推荐)"
echo "------------------------"
echo "如果 Python Workers 不可用，可以使用 Docker 部署:"
echo "1. 构建 Docker 镜像: docker build -t watch-ricon-stock ."
echo "2. 推送到容器仓库"
echo "3. 在 Cloudflare 中部署容器镜像"

echo
echo "部署准备完成！"