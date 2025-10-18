#!/bin/bash
# Cloudflare 部署脚本

set -e  # 遇到错误时停止脚本

echo "开始部署 watch-ricon-stock 到 Cloudflare..."

# 检查必要工具
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装或不可用"
    exit 1
fi

if ! command -v wrangler &> /dev/null; then
    echo "警告: wrangler 未安装，跳过 Workers 部署"
    echo "安装 wrangler: npm install -g wrangler"
fi

# 构建 Docker 镜像
echo "构建 Docker 镜像..."
docker build -t watch-ricon-stock .

# 运行本地测试
echo "运行本地测试..."
docker run -d -p 5000:5000 --name watch-ricon-stock-test watch-ricon-stock

echo "应用正在本地运行，访问 http://localhost:5000"
echo "测试完成后，使用 'docker stop watch-ricon-stock-test && docker rm watch-ricon-stock-test' 停止容器"

echo "部署准备完成!"
echo "要部署到 Cloudflare Container:"
echo "1. 上传镜像到容器注册表"
echo "2. 在 Cloudflare Dashboard 中部署"