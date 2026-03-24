# 🚀 快速部署指南

## ✅ 已完成的工作

已经为您创建了完整的自动更新系统，包括：

### 1. 数据文件（`data/` 目录）
- `quotes.json` - 20 条经典金句
- `stories.json` - 15 个历史故事
- `messages.json` - 20 条行动建议
- `news.json` - 新闻数据（自动更新）

### 2. Python 脚本（`scripts/` 目录）
- `fetch_news.py` - 新闻爬虫（含默认数据）
- `generate_content.py` - 每日励志内容生成
- `update_site.py` - 主更新脚本

### 3. GitHub Actions 工作流
- `.github/workflows/daily-update.yml` - 每天北京时间 8:00 自动运行

### 4. 配置文件
- `requirements.txt` - Python 依赖

## 📋 部署步骤

### 步骤 1：推送到 GitHub

打开终端，执行以下命令：

```bash
# 初始化 git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始化晨间励志网站 - 自动更新系统"

# 创建新的 GitHub 仓库（在 GitHub 网站上操作）
# 然后添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 推送到 main 分支
git push -u origin main
```

### 步骤 2：启用 GitHub Actions

1. 打开你的 GitHub 仓库页面
2. 点击顶部的 **"Actions"** 标签
3. 如果看到安全提示，点击 **"I understand my workflows, go ahead and enable them"**
4. 确认工作流已启用（绿色圆点）

### 步骤 3：测试自动更新

#### 方法 1：手动触发工作流

1. 在 GitHub 仓库，进入 **Actions** 标签
2. 点击左侧的 **"每日自动更新晨间励志内容"**
3. 点击 **"Run workflow"** 按钮
4. 选择分支（main），点击 **"Run workflow"**
5. 等待 1-2 分钟，查看运行结果
6. 刷新仓库页面，查看 `index.html` 是否更新

#### 方法 2：等待自动运行

工作流会在每天 **北京时间 8:00** 自动运行（UTC 时间 0:00）

### 步骤 4：启用 GitHub Pages（在线访问）

1. 进入仓库的 **Settings** 页面
2. 左侧菜单点击 **"Pages"**
3. **Source** 选择：**"Deploy from a branch"**
4. **Branch** 选择：**"main"**，文件夹选择：**"/ (root)"**
5. 点击 **"Save"**

等待 2-3 分钟后，访问：
```
https://你的用户名.github.io/仓库名/
```

## 🔍 验证部署

### 检查 GitHub Actions 是否正常运行

1. 进入 **Actions** 标签
2. 查看最近的工作流运行记录
3. 绿色 ✅ 表示成功，红色 ❌ 表示失败

### 检查内容是否更新

1. 打开 `index.html` 文件
2. 查看日期是否更新
3. 查看金句、故事、新闻是否变化

### 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 手动运行更新
python scripts/update_site.py

# 启动本地服务器
python -m http.server 8000
```

访问：http://localhost:8000

## ⚙️ 自定义配置

### 修改更新时间

编辑 `.github/workflows/daily-update.yml`：

```yaml
on:
  schedule:
    # 修改这里的 cron 表达式
    # 分 时 日 月 星期（UTC 时间）
    - cron: '0 0 * * *'  # 北京时间 8:00
```

常用时间：
- 6:00 → `0 22 * * *`（前一天 UTC 22:00）
- 7:00 → `0 23 * * *`（前一天 UTC 23:00）
- 8:00 → `0 0 * * *`（UTC 0:00）
- 9:00 → `0 1 * * *`（UTC 1:00）

### 添加更多内容

编辑 `data/` 目录下的 JSON 文件，按照现有格式添加新内容。

## 🛠️ 故障排查

### 问题 1：GitHub Actions 运行失败

**解决方案：**
1. 点击失败的运行记录
2. 查看错误日志
3. 检查 `.github/workflows/daily-update.yml` 语法
4. 确保 `requirements.txt` 包含所有依赖

### 问题 2：内容没有更新

**解决方案：**
1. 检查 Actions 是否成功运行
2. 查看 git 提交历史，确认有更新提交
3. 手动触发工作流测试

### 问题 3：GitHub Pages 无法访问

**解决方案：**
1. 等待 3-5 分钟（首次部署需要时间）
2. 检查 Pages 设置是否正确
3. 确认 `index.html` 在仓库根目录

### 问题 4：新闻抓取失败

**说明：** 脚本内置了默认新闻数据，即使抓取失败也会正常显示。

## 📞 获取帮助

如果遇到问题：

1. 查看 GitHub Actions 日志
2. 检查文件路径和语法
3. 参考 README.md 详细说明

## 🎉 完成！

现在你的晨间励志网站已经部署完成，每天早晨 8 点自动更新内容！

访问你的网站，开始新一天的励志之旅吧！🌅💪
