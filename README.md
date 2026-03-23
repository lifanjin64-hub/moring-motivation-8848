# 晨间励志创业鼓励 - 自动更新系统

这是一个每天早晨 8 点自动更新的励志创业鼓励网站，包含每日金句、历史故事、创业寄语和热门财经新闻。

## 📋 功能特性

- ✅ **每日自动更新**：每天北京时间 8:00 自动更新内容
- ✅ **励志内容**：精选 20 条金句、15 个历史故事、20 条行动建议
- ✅ **热门新闻**：自动抓取财联社、新浪财经、微博的热门财经新闻
- ✅ **精美界面**：响应式设计，渐变色彩，动画效果
- ✅ ** GitHub Actions**：使用 GitHub 定时任务自动运行

## 🚀 部署步骤

### 1. 推送到 GitHub

```bash
# 初始化 git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始化晨间励志网站"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 推送
git push -u origin main
```

### 2. 启用 GitHub Actions

1. 在 GitHub 仓库页面，点击 "Actions" 标签
2. 点击 "I understand my workflows, go ahead and enable them"
3. 确认 `daily-update.yml` 工作流已启用

### 3. 配置 GitHub Pages（可选，用于在线访问）

1. 进入仓库 Settings
2. 点击左侧 "Pages"
3. Source 选择 "Deploy from a branch"
4. Branch 选择 "main"，文件夹选择 "/ (root)"
5. 点击 "Save"

几分钟后，你的网站将在 `https://你的用户名.github.io/仓库名/` 上线

### 4. 测试自动更新

你可以手动触发工作流来测试：

1. 进入 GitHub 仓库的 "Actions" 标签
2. 点击 "每日自动更新晨间励志内容" 工作流
3. 点击 "Run workflow" 按钮
4. 选择分支，点击 "Run workflow"
5. 等待工作流完成，检查 index.html 是否更新

## 📁 项目结构

```
morning-motivation/
├── .github/
│   └── workflows/
│       └── daily-update.yml    # GitHub Actions 定时任务配置
├── data/
│   ├── quotes.json            # 金句数据（20 条）
│   ├── stories.json           # 历史故事数据（15 个）
│   ├── messages.json          # 行动建议数据（20 条）
│   └── news.json              # 新闻数据（自动更新）
├── scripts/
│   ├── fetch_news.py          # 新闻爬虫脚本
│   ├── generate_content.py    # 励志内容生成脚本
│   └── update_site.py         # 主更新脚本
├── index.html                 # 网站主页面
├── requirements.txt           # Python 依赖
└── README.md                  # 项目说明
```

## 🔧 本地测试

### 安装依赖

```bash
pip install -r requirements.txt
```

### 手动运行更新

```bash
python scripts/update_site.py
```

### 启动本地服务器

```bash
python -m http.server 8000
```

然后在浏览器访问：http://localhost:8000

## 📝 自定义内容

### 添加更多金句

编辑 `data/quotes.json`，按照格式添加新的金句：

```json
{
  "text": "你的金句内容",
  "author": "作者或出处"
}
```

### 添加更多历史故事

编辑 `data/stories.json`，按照格式添加新的故事：

```json
{
  "title": "故事标题",
  "content": ["段落 1", "段落 2"],
  "highlight": "关键词"
}
```

### 添加更多行动建议

编辑 `data/messages.json`，按照格式添加新的建议：

```json
{
  "title": "今日行动建议",
  "content": "建议内容"
}
```

## 🕐 修改更新时间

如果需要修改更新时间（默认北京时间 8:00），编辑 `.github/workflows/daily-update.yml`：

```yaml
on:
  schedule:
    # cron 表达式：分 时 日 月 星期
    # UTC 时间 0:00 = 北京时间 8:00
    - cron: '0 0 * * *'
```

常用时间：
- 北京时间 6:00：`0 22 * * *`（前一天 UTC 22:00）
- 北京时间 7:00：`0 23 * * *`（前一天 UTC 23:00）
- 北京时间 8:00：`0 0 * * *`（UTC 0:00）
- 北京时间 9:00：`0 1 * * *`（UTC 1:00）

## 🛠️ 故障排查

### GitHub Actions 运行失败

1. 检查 `.github/workflows/daily-update.yml` 语法是否正确
2. 查看 Actions 日志，确认错误信息
3. 确保 `requirements.txt` 包含所有需要的依赖

### 新闻抓取失败

脚本已内置默认新闻数据，即使抓取失败也会使用默认数据，确保网站正常显示。

### 内容不更新

1. 检查工作流是否正常运行
2. 查看提交历史，确认是否有新的提交
3. 手动触发工作流测试

## 📄 许可证

MIT License

## 🙏 致谢

感谢使用晨间励志创业鼓励系统！

祝你在创业路上一路顺风，旗开得胜！🌅💪
