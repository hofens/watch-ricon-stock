# 关于远程仓库设置

## 如何设置远程仓库

### 1. 在GitHub上创建新仓库
1. 打开浏览器，访问 https://github.com
2. 登录您的GitHub账户
3. 点击右上角的 "+" 号，然后选择 "New repository"
4. 填写仓库信息：
   - Repository name: `watch-ricon-stock`
   - Description: `Ricn Mall Stock Monitor - Monitor product listings and stock changes`
   - Public (推荐) 或 Private
   - **不勾选** "Initialize this repository with a README"
   - **不勾选** "Add .gitignore"（项目中已有）
   - **不勾选** "Choose a license"（项目中已有）

### 2. 连接本地仓库到远程仓库
在项目目录中打开命令行，执行以下命令（将URL替换为您创建的仓库地址）：

```bash
git remote add origin https://github.com/您的用户名/watch-ricon-stock.git
```

### 3. 验证连接
```bash
git remote -v
```

### 4. 推送到远程仓库
```bash
git push -u origin master
```

## 安全说明

此项目已经过安全处理：
- 配置文件中不包含任何敏感信息
- .gitignore 文件已配置为忽略包含敏感信息的文件
- 所有密码和邮箱信息都使用占位符

## 项目使用说明

1. 克隆仓库：
   ```bash
   git clone https://github.com/您的用户名/watch-ricon-stock.git
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置（首次使用）：
   - 复制 `src/config.json` 为 `src/config.local.json`
   - 修改配置文件以适应您的需求

4. 运行程序：
   ```bash
   python src/product_monitor.py --config src/config.local.json
   ```

## Git连接问题解决（如果遇到连接错误）

如果您在推送代码时遇到类似错误：
```
Failed to connect to 127.0.0.1 port 7890 after 2080 ms: Connection refused
```

请参考 `GIT_PROXY_FIX.md` 文件中的解决方法。

## 项目文档

- 英文文档：README.md
- 中文文档：README.zh.md
- 代理问题解决：GIT_PROXY_FIX.md