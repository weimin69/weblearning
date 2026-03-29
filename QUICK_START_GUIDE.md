# ⚡ 5分钟快速开始指南

## 第一步：环境准备 (1分钟)

```bash
# 1. 确保已安装Python 3.8+
python3 --version

# 2. 克隆或下载项目
# 如果你从GitHub下载，直接进入项目目录
cd weblearning
```

## 第二步：一键启动 (1分钟)

```bash
# 给启动脚本添加执行权限
chmod +x start_all_platforms.sh

# 运行启动脚本
./start_all_platforms.sh
```

## 第三步：选择模式 (1分钟)

启动脚本会显示菜单：
```
选择运行模式：
1. 跨平台刷课系统 (推荐)
2. 原智慧树刷课脚本
3. 测试浏览器兼容性
4. 退出
```

**选择选项1**，系统会自动：
- ✅ 创建虚拟环境
- ✅ 安装Python依赖
- ✅ 检查浏览器驱动

## 第四步：配置参数 (1分钟)

按提示输入：
1. **课程页面URL** - 复制你的课程链接
2. **浏览器类型** - 推荐选择1 (Chrome)
3. **是否无头模式** - 新手选n (显示浏览器)
4. **登录信息** - 可选，不填则手动登录
5. **刷课时长** - 默认60分钟

## 第五步：开始刷课 (立即开始)

确认配置后，系统自动：
1. 🚀 打开浏览器并登录
2. 🎬 跳转到课程页面
3. ▶️ 开始播放第一个视频
4. 🔍 监控题目弹窗
5. 📊 显示实时进度

## 🆘 遇到问题？

### 0. ModuleNotFoundError: No module named 'selenium'
```bash
# 错误原因：没有激活虚拟环境
# 解决方法：
source venv/bin/activate
# 现在再运行 python3 cross_platform_course.py
```

### 1. 浏览器无法打开
```bash
# 运行浏览器测试
./start_all_platforms.sh  # 选择选项3
```

### 2. 依赖安装失败
```bash
# 手动安装（在虚拟环境中）
source venv/bin/activate
pip install selenium webdriver-manager
```

### 3. 需要更多帮助
查看完整文档：
```bash
# 阅读完整README
cat README.md | less
```

## 🎯 高级用法

### 配置文件方式 (推荐)
```bash
# 1. 复制配置文件
cp config_example.py config.py

# 2. 编辑配置文件
# 修改 course_url、username 等

# 3. 快速启动
python3 quick_start.py
```

### 无头模式 (后台运行)
```bash
# 在配置中设置或运行时选择
"headless": True
```

### 自定义选择器
如果默认选择器不工作，在 `config.py` 中添加：
```python
CUSTOM_SELECTORS = {
    "play_buttons": [".your-play-button"],
    "question_popups": [".your-question-popup"],
}
```

## 📊 监控进度

刷课过程中会显示：
```
已运行 15 分钟，剩余 45 分钟
播放了 3 个视频，处理了 2 个题目
```

## ⏸️ 停止刷课

- 按 `Ctrl+C` 停止脚本
- 浏览器会自动关闭
- 进度信息会保存

## 🔄 重新开始

```bash
# 再次运行
./start_all_platforms.sh

# 或直接运行
python3 cross_platform_course.py
```

## 🎉 完成！

你现在已经成功设置了跨平台刷课系统。系统会自动处理：

✅ **视频播放** - 自动开始和继续播放  
✅ **题目处理** - 检测、答题、关闭弹窗  
✅ **连续播放** - 视频结束自动播放下一个  
✅ **进度监控** - 实时显示刷课状态  

享受自动化刷课的便利吧！ 🚀