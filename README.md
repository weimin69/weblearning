# 🌐 跨平台刷课自动化系统

一个支持所有主流浏览器和刷课平台的全自动刷课系统，可以自动播放视频、处理题目、连续播放下一个视频。

## ✨ 核心功能

### ✅ 支持的学习平台
- **智慧树** (zhihuishu.com) - 主要支持
- **超星学习通** (chaoxing.com) - 完全支持
- **知到** (zhihuishu.com) - 完全支持
- **其他平台** - 基础支持，可自定义

### ✅ 支持的浏览器
- **Chrome** - 推荐使用，兼容性最好
- **Firefox** - 开源浏览器支持
- **Edge** - Windows/macOS 原生支持
- **Safari** - macOS 原生支持

### ✅ 智能自动化
- **自动播放视频** - 智能检测并点击播放按钮
- **题目检测与处理** - 实时监控题目弹窗
- **随机答案选择** - 单选题/多选题智能处理
- **自动关闭弹窗** - 答题后自动关闭题目窗口
- **连续视频播放** - 视频结束后自动播放下一个
- **状态监控** - 实时显示刷课进度

### ✅ 跨平台兼容
- **macOS** - 完全支持
- **Linux** - 完全支持
- **Windows** - 通过WSL或原生支持
- **无头模式** - 后台运行，不显示浏览器界面

## 🚀 快速开始

### 1. 环境准备

#### 1.1 安装浏览器（至少安装一个）
```bash
# macOS 使用 Homebrew
brew install --cask google-chrome    # 安装Chrome
brew install --cask firefox          # 安装Firefox

# 或从官网下载：
# Chrome: https://www.google.com/chrome/
# Firefox: https://www.mozilla.org/firefox/
```

#### 1.2 克隆项目并安装依赖
```bash
# 克隆项目
git clone <你的仓库地址>
cd weblearning

# 运行启动脚本（自动安装Python依赖和浏览器驱动）
chmod +x start_all_platforms.sh
./start_all_platforms.sh
```

#### 1.3 虚拟环境中的浏览器驱动
脚本使用 `webdriver-manager` 自动管理浏览器驱动，无需手动安装。驱动会自动下载到虚拟环境中。

### 2. 激活虚拟环境（重要！）

在运行任何Python脚本之前，必须先激活虚拟环境：

```bash
# 激活虚拟环境
source venv/bin/activate

# 激活后，命令行前面会显示 (venv)
(venv) weblearning$ 
```

如果看到 `ModuleNotFoundError: No module named 'selenium'` 错误，说明没有激活虚拟环境。

### 3. 操作模式选择

运行脚本时，可以选择两种操作模式：

#### **手动模式（推荐）**
- 用户先手动选择要刷的视频
- 手动点击播放按钮开始播放
- 脚本自动处理题目和播放下一个视频
- **优点**：更稳定，避免误判

#### **自动模式**
- 脚本自动播放第一个视频
- 全自动化处理
- **注意**：可能需要调整检测参数

### 4. 配置使用

**方式一：交互式使用（推荐新手）**
```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 运行主程序（推荐选择手动模式）
python3 cross_platform_course.py
```

**方式二：配置文件使用**
```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 复制配置文件
cp config_example.py config.py

# 3. 编辑配置文件
# 修改 course_url、username、password 等配置

# 4. 快速启动
python3 quick_start.py
```

**方式三：使用启动脚本（最简单）**
```bash
# 启动脚本会自动处理虚拟环境
./start_all_platforms.sh
# 选择选项1：跨平台刷课系统
```

**方式三：命令行直接使用**
```bash
python3 cross_platform_course.py
# 按提示输入课程URL、浏览器类型、登录信息等
```

## 📋 系统要求

### 基础要求
- Python 3.8+
- 稳定的网络连接
- 至少一种主流浏览器

### 浏览器要求
| 浏览器 | macOS | Linux | Windows | 备注 |
|--------|-------|-------|---------|------|
| Chrome | ✅ 推荐 | ✅ 推荐 | ✅ 推荐 | 兼容性最好 |
| Firefox | ✅ 支持 | ✅ 支持 | ✅ 支持 | 开源选择 |
| Edge | ✅ 支持 | ⚠️ 有限 | ✅ 支持 | Windows/macOS |
| Safari | ✅ 支持 | ❌ 不支持 | ❌ 不支持 | 仅macOS |

### 驱动安装
系统会自动检测驱动，如需手动安装：

**macOS:**
```bash
# Chrome
brew install --cask chromedriver

# Firefox
brew install geckodriver

# Edge
brew install --cask microsoft-edge
```

**Linux (Ubuntu/Debian):**
```bash
# Chrome
sudo apt install chromium-chromedriver

# Firefox
sudo apt install firefox-geckodriver
```

**Windows:**
- 下载对应浏览器的驱动
- 添加到系统PATH环境变量
- 或使用 `webdriver-manager` 自动管理

## 🔧 详细配置

### 配置文件说明
编辑 `config.py` 文件：

```python
COURSE_CONFIG = {
    # 必填：课程页面URL
    "course_url": "https://www.zhihuishu.com/你的课程页面",
    
    # 可选：登录信息（不填则手动登录）
    "username": "你的用户名",
    "password": "你的密码",
    
    # 刷课时长（分钟）
    "duration_minutes": 60,
    
    # 浏览器配置
    "browser": "chrome",  # chrome, firefox, edge, safari
    "headless": False,    # 是否无头模式运行
    
    # 高级配置
    "check_interval": 15,     # 检查题目间隔(秒)
    "video_check_interval": 10,  # 检查视频结束间隔(秒)
    "status_interval": 30,    # 状态报告间隔(秒)
}
```

### 自定义选择器
如果默认选择器不工作，可以在 `config.py` 中添加自定义选择器：

```python
CUSTOM_SELECTORS = {
    "play_buttons": [".custom-play-btn", "#video-play-button"],
    "question_popups": [".custom-question-popup"],
    "answer_options": [".custom-option"],
    "next_video_buttons": [".custom-next-btn"],
    "close_buttons": [".custom-close-btn"],
}
```

## 🎯 使用步骤

### 第一步：准备课程
1. 登录你的学习平台（如智慧树）
2. 进入要刷的课程页面
3. 复制浏览器地址栏的URL

### 第二步：运行脚本
```bash
# 方法1：使用启动脚本
./start_all_platforms.sh

# 方法2：直接运行
python3 cross_platform_course.py
```

### 第三步：配置参数
脚本会询问以下信息：
1. **课程页面URL** - 粘贴你复制的URL
2. **浏览器类型** - 选择使用的浏览器
3. **是否无头模式** - 是否显示浏览器界面
4. **登录信息** - 用户名和密码（可选）
5. **刷课时长** - 分钟数（默认60分钟）

### 第四步：开始刷课
确认配置后，系统会自动：
1. 打开选择的浏览器
2. 登录平台（如果配置了登录信息）
3. 跳转到课程页面
4. 开始播放第一个视频
5. 监控并处理弹出的题目
6. 视频结束后自动播放下一个视频
7. 显示实时刷课进度

## 🔍 工作原理

### 视频播放检测
```python
# 检测视频是否在播放
if not video_is_playing():
    click_play_button()
    
# 检测视频是否结束
if video_is_ended():
    click_next_video_button()
```

### 题目处理流程
1. **检测题目弹窗** - 每15秒检查一次
2. **随机选择答案** - 智能识别单选/多选
3. **提交答案** - 自动点击提交按钮
4. **关闭弹窗** - 答题后关闭题目窗口
5. **恢复播放** - 重新播放视频

### 连续播放机制
1. **视频结束检测** - 每10秒检查视频进度
2. **下一个视频查找** - 智能识别"下一节"按钮
3. **自动跳转** - 点击下一个视频链接
4. **新视频播放** - 自动开始播放新视频

## 🛠️ 故障排除

### 常见问题

**0. ModuleNotFoundError: No module named 'selenium'**
```bash
# 错误原因：没有激活虚拟环境
# 解决方法：
cd /Users/alax/weblearning
source venv/bin/activate
# 现在再运行 python3 cross_platform_course.py
```

**1. 浏览器无法打开或驱动错误**
```bash
# 1. 确保已安装浏览器（Chrome/Firefox等）
# 2. 运行测试检查驱动
./start_all_platforms.sh  # 选择选项3测试浏览器

# 3. 如果测试失败，手动安装驱动：
source venv/bin/activate
python3 -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

**2. 浏览器打开后空白或没有进入网站**
```bash
# 运行页面加载诊断
python3 test_page_load.py

# 常见原因和解决方法:
# 1. 网络问题 - 检查网络连接
# 2. DNS问题 - 检查DNS设置
# 3. 网站限制 - 手动访问确认
# 4. 验证码 - 可能需要手动验证
```

**3. 页面加载失败或超时**
- 脚本会自动重试3次
- 检查课程URL是否正确
- 确保网络连接稳定
- 如果是"其他平台"，需要手动登录
- 尝试使用无头模式测试

**2. 无法检测题目**
- 平台页面可能已更新
- 尝试添加自定义选择器
- 检查网络连接是否稳定

**3. 视频无法自动播放**
- 尝试关闭广告拦截器
- 检查浏览器是否允许自动播放
- 尝试使用无头模式

**4. 登录失败**
- 检查用户名密码是否正确
- 选择手动登录模式
- 确保验证码已通过

### 调试模式
```bash
# 修改配置文件，关闭无头模式
"headless": False

# 观察浏览器操作，查看问题所在
```

## 📊 状态监控

刷课过程中会显示实时状态：
```
已运行 15 分钟，剩余 45 分钟
播放了 3 个视频，处理了 2 个题目
```

### 状态说明
- **运行时间** - 已刷课时长
- **剩余时间** - 预计结束时间
- **视频计数** - 已播放的视频数量
- **题目计数** - 已处理的题目数量

## ⚙️ 高级功能

### 无头模式
```python
# 配置文件设置
"headless": True

# 或命令行选择
# 是否使用无头模式？(y/n): y
```

### 自定义检查间隔
```python
# 配置文件调整
"check_interval": 10,      # 题目检查间隔（秒）
"video_check_interval": 5, # 视频检查间隔（秒）
"status_interval": 60,     # 状态报告间隔（秒）
```

### 多浏览器支持
```python
# 运行时选择浏览器
# 选择浏览器:
# 1. Chrome (推荐)
# 2. Firefox
# 3. Edge
# 4. Safari (仅macOS)
```

## 🔒 安全提示

### 重要注意事项
⚠️ **请遵守平台使用规定**
- 本工具仅用于学习自动化技术
- 请勿用于违反平台规则的行为
- 建议在个人学习时使用
- 尊重知识产权和课程内容

### 隐私保护
- 登录信息仅用于自动化登录
- 不会保存或上传任何个人信息
- 建议使用课程专用账号
- 刷课结束后及时退出登录

## 📁 项目结构

```
weblearning/
├── cross_platform_course.py    # 主程序 - 跨平台刷课系统
├── auto_course.py              # 原版 - 智慧树刷课脚本
├── quick_start.py              # 快速启动脚本
├── config_example.py           # 配置文件示例
├── requirements.txt            # Python依赖
├── start_all_platforms.sh      # 跨平台启动脚本
├── start.sh                    # 原版启动脚本
├── README_FULL.md              # 完整文档（本文件）
├── README.md                   # 原版文档
└── ...其他测试文件
```

## 🆘 技术支持

### 问题反馈
1. 检查是否按照文档步骤操作
2. 查看控制台错误信息
3. 尝试不同的浏览器
4. 调整检查间隔参数

### 无法解决的问题
- 平台大规模改版
- 复杂的验证码机制
- 需要人工干预的环节
- 网络连接不稳定

## 📄 许可证

本项目仅供学习和技术研究使用，使用者需自行承担使用风险。

### 免责声明
- 请遵守相关平台的使用条款
- 请遵守当地法律法规
- 尊重课程版权和知识产权
- 合理使用自动化工具

## 🎉 开始使用

```bash
# 最简单的开始方式
chmod +x start_all_platforms.sh
./start_all_platforms.sh

# 选择选项1，按提示操作
# 享受自动化刷课的便利！
```

---

**提示**: 首次使用建议先运行浏览器兼容性测试，确保环境配置正确。

**更新**: 如有新功能或修复，请查看 `UPDATES.md` 文件。

**贡献**: 欢迎提交Issue和Pull Request改进项目。