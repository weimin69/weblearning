# GitHub 仓库设置指南

## 仓库准备步骤

### 1. 创建新的GitHub仓库
1. 登录GitHub
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - **Repository name**: `weblearning-auto-course` (或你喜欢的名称)
   - **Description**: `跨平台刷课自动化系统 - 支持Chrome/Firefox/Edge/Safari`
   - **Visibility**: Public (推荐) 或 Private
   - **Initialize with**: 不要勾选任何选项（我们已有文件）
4. 点击 "Create repository"

### 2. 本地Git初始化
```bash
cd /Users/alax/weblearning

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交初始版本
git commit -m "初始提交: 跨平台刷课自动化系统 v2.0.0

- 支持所有主流浏览器 (Chrome, Firefox, Edge, Safari)
- 跨平台兼容 (macOS, Linux, Windows)
- 智能题目检测与随机答案选择
- 自动连续视频播放
- 配置文件系统和快速启动脚本
- 完整的文档和测试工具"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/仓库名称.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

## 仓库文件结构说明

```
weblearning-auto-course/
├── cross_platform_course.py    # 🎯 主程序 - 跨平台刷课系统
├── auto_course.py              # 🔧 原版 - 智慧树刷课脚本
├── quick_start.py              # ⚡ 快速启动脚本
├── config_example.py           # ⚙️ 配置文件示例
├── requirements.txt            # 📦 Python依赖
├── start_all_platforms.sh      # 🚀 跨平台启动脚本
├── start.sh                    # 🔧 原版启动脚本
├── test_system.py              # ✅ 系统测试工具
├── README_FULL.md              # 📖 完整使用文档
├── README.md                   # 📄 原版文档
├── UPDATES.md                  # 🔄 更新日志
├── GITHUB_SETUP.md             # 🛠️ 本文件 - GitHub设置指南
├── QUICK_START.md              # 🏃 快速开始指南
└── ...其他测试文件
```

## 推荐的仓库设置

### 1. 添加仓库主题
在仓库页面点击 "Manage topics"，添加：
- `automation`
- `selenium`
- `web-automation`
- `course-automation`
- `python`
- `browser-automation`

### 2. 添加README徽章
在 `README_FULL.md` 顶部添加：

```markdown
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-green)
![Browsers](https://img.shields.io/badge/browsers-Chrome%20%7C%20Firefox%20%7C%20Edge%20%7C%20Safari-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
```

### 3. 添加许可证文件
创建 `LICENSE` 文件：

```markdown
MIT License

Copyright (c) 2025 [你的名字]

Permission is hereby granted...
```

### 4. 添加 .gitignore 文件
创建 `.gitignore` 文件：

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
.venv/

# Config files
config.py
*.env
*.secret

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
```

## 发布说明

### 版本标签
```bash
# 创建版本标签
git tag -a v2.0.0 -m "跨平台刷课系统 v2.0.0"

# 推送标签到GitHub
git push origin v2.0.0
```

### 发布版本
1. 在GitHub仓库页面点击 "Releases"
2. 点击 "Draft a new release"
3. 填写版本信息：
   - **Tag version**: `v2.0.0`
   - **Release title**: `跨平台刷课系统 v2.0.0`
   - **Description**: 复制 `UPDATES.md` 中的v2.0.0内容
4. 点击 "Publish release"

## 推广建议

### 1. 编写项目介绍
在README开头添加简洁介绍：

```markdown
# 🌐 跨平台刷课自动化系统

一个支持所有主流浏览器的全自动刷课系统，可以：
- ✅ 自动播放视频课程
- ✅ 智能处理题目弹窗
- ✅ 连续播放下一个视频
- ✅ 支持 Chrome, Firefox, Edge, Safari
- ✅ 兼容 macOS, Linux, Windows

🚀 **一键启动** | ⚡ **全自动化** | 🔒 **安全可靠**
```

### 2. 添加使用示例
```markdown
## 🎯 快速体验

```bash
# 克隆项目
git clone https://github.com/你的用户名/仓库名称.git
cd 仓库名称

# 一键启动
chmod +x start_all_platforms.sh
./start_all_platforms.sh
```

### 3. 添加功能演示
考虑添加：
- 屏幕录制GIF展示功能
- 终端输出截图
- 架构图或流程图

## 维护建议

### 1. 问题模板
在 `.github/ISSUE_TEMPLATE/` 目录创建问题模板：

**bug_report.md**:
```markdown
---
name: Bug报告
about: 报告系统bug
title: '[BUG] '
labels: bug
---

## 问题描述
清晰描述问题...

## 重现步骤
1. ...
2. ...
3. ...

## 预期行为
应该发生什么...

## 实际行为
实际发生了什么...

## 环境信息
- 操作系统: [如 macOS 12.0]
- Python版本: [如 3.9.0]
- 浏览器: [如 Chrome 91]
- 脚本版本: [如 v2.0.0]
```

### 2. Pull Request模板
创建 `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## 变更描述
描述这次PR的变更...

## 变更类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 其他

## 测试
- [ ] 已通过现有测试
- [ ] 添加了新测试
- [ ] 手动测试通过

## 相关Issue
关闭 #issue_number
```

## 安全注意事项

### 1. 敏感信息
- 不要提交 `config.py` 文件（已添加到.gitignore）
- 不要在代码中硬编码密码
- 使用环境变量或配置文件

### 2. 使用条款
在README中添加：

```markdown
## ⚠️ 免责声明

本工具仅供学习自动化技术使用，请遵守：
1. 相关平台的使用条款
2. 当地法律法规
3. 尊重课程版权

使用者需自行承担使用风险。
```

## 下一步行动

1. **立即操作**:
   ```bash
   # 初始化Git仓库并推送
   git init
   git add .
   git commit -m "初始提交"
   git remote add origin [你的仓库URL]
   git push -u origin main
   ```

2. **完善文档**:
   - 更新README中的仓库链接
   - 添加更多使用示例
   - 创建视频教程（可选）

3. **社区建设**:
   - 回复Issue和PR
   - 接受贡献
   - 定期更新版本

4. **推广分享**:
   - 在技术社区分享
   - 写博客文章介绍
   - 收集用户反馈

## 成功指标

- ⭐ Star数量增长
- 🍴 Fork数量增加
- 📈 Issue和PR活跃
- 👥 用户社区形成

祝你的项目成功！🎉