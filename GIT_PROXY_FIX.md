# Git连接问题解决指南

## 问题描述
您可能在使用代理工具（如Clash、Shadowsocks等）时遇到以下错误：
```
fatal: unable to access 'https://github.com/yourusername/watch-ricon-stock.git/': Failed to connect to 127.0.0.1 port 7890 after 2080 ms: Connection refused
```

这通常是由于Git继承了系统代理设置导致的。

## 解决方法

### 方法1：临时禁用Git代理（推荐）
```bash
# 禁用Git的HTTP/HTTPS代理
git config --global --unset http.proxy
git config --global --unset https.proxy

# 然后尝试推送
git push -u origin master
```

### 方法2：为GitHub配置代理例外
如果您需要保留代理设置，可以为GitHub配置例外：
```bash
# 配置GitHub不需要代理
git config --global http.https://github.com.proxy ""
```

### 方法3：检查系统代理设置
在Windows系统中：
1. 打开"设置" → "网络和Internet" → "代理"
2. 检查是否有代理设置被启用
3. 临时禁用代理，完成Git操作后再重新启用

### 方法4：使用SSH方式（长期解决方案）
配置SSH密钥并使用SSH URL进行推送：

1. 生成SSH密钥：
```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

2. 添加SSH密钥到ssh-agent：
```bash
ssh-add ~/.ssh/id_rsa
```

3. 将公钥添加到GitHub账户（复制 ~/.ssh/id_rsa.pub 的内容到GitHub SSH密钥设置）

4. 更改远程仓库URL为SSH方式：
```bash
git remote set-url origin git@github.com:yourusername/watch-ricon-stock.git
```

## 验证连接
测试连接是否正常：
```bash
# 测试HTTPS连接
curl -I https://github.com

# 测试SSH连接（如果使用SSH方式）
ssh -T git@github.com
```

## 项目安全提醒
- 确保在推送前检查 `.gitignore` 是否正确配置
- 配置文件不包含敏感信息
- 在推送到公共仓库前确认没有敏感数据