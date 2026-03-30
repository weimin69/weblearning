# 学习通功能更新文档

## 📋 更新概述

已成功为学习通（超星）平台添加了完整的防挂机检测绕过功能，解决了鼠标移出浏览器范围导致视频停止播放的问题。

## 🚀 新增功能

### 1. 自动登录系统
- **功能**: 支持学习通用户名密码自动登录
- **方法**: `_login_chaoxing()`
- **特点**: 智能查找登录表单，无需手动干预

### 2. 视频完成检测
- **功能**: 检测右侧视频选择栏的对勾标记
- **方法**: `_check_chaoxing_video_completed()`
- **特点**: 智能识别视频播放完成状态

### 3. 题目解答系统
- **功能**: 智能检测和解答视频中的问题
- **方法**: `_answer_chaoxing_question()`
- **特点**: 支持单选、多选和随机答案选择

### 4. 视频恢复播放
- **功能**: 答题后自动恢复视频播放
- **方法**: `resume_video_playback()`
- **特点**: 多种恢复机制确保播放连续性

### 5. 播放下一个视频
- **功能**: 视频完成后自动播放下一个
- **方法**: `_go_to_next_chaoxing_video()`
- **特点**: 支持课程目录导航和智能查找

## 🛡️ 防挂机检测绕过系统（新增）

### 多层保护机制

#### 1. 定期绕过系统 (每25-35秒)
- **方法**: `_bypass_chaoxing_anti_idle()`
- **包含**:
  - 模拟鼠标移动 (`_simulate_mouse_activity()`)
  - 模拟键盘活动 (`_simulate_keyboard_activity()`)
  - 保持页面激活 (`_keep_page_active()`)
  - 检查恢复视频 (`_check_and_resume_video()`)

#### 2. 轻量级活动模拟 (每10秒)
- **方法**: `_simulate_light_activity()`
- **包含**:
  - 鼠标悬停模拟 (`_simulate_mouse_hover()`)
  - 轻微滚动 (`_simulate_scroll_slight()`)
  - 文档活动 (`_simulate_document_activity()`)
  - 窗口焦点 (`_simulate_window_focus()`)

#### 3. JavaScript注入保护
- **方法**: `_init_anti_idle_protection()`
- **功能**:
  - 重写 `document.hasFocus()` 方法
  - 监控页面可见性状态
  - 定期更新活动时间戳
  - 注入全局活动监控

#### 4. 弹窗检测与处理
- **方法**: `_check_for_idle_popup()`
- **功能**:
  - 检测挂机警告弹窗
  - 自动关闭警告对话框
  - 恢复正常播放状态

## ⚙️ 技术实现细节

### 监控循环集成
```python
# 在 monitor_simple() 方法中集成
if self.platform_type == PlatformType.CHAOXING:
    # 每25-35秒执行完整绕过
    if current_time - last_bypass_time > random.randint(25, 35):
        self._bypass_chaoxing_anti_idle()
        last_bypass_time = current_time
    
    # 每10秒执行轻量级活动
    if current_time - last_activity_time > 10:
        self._simulate_light_activity()
        last_activity_time = current_time
```

### 随机化策略
- **时间间隔随机化**: 避免固定模式被检测
- **活动类型随机化**: 模拟真实用户行为
- **检查间隔随机化**: 8-12秒随机间隔

## 🎯 解决的问题

1. **鼠标移出检测**: 通过模拟鼠标活动保持页面激活
2. **页面非激活状态**: 重写焦点检测方法，保持页面"有焦点"
3. **挂机警告弹窗**: 自动检测并关闭警告对话框
4. **视频暂停问题**: 定期检查并恢复视频播放
5. **行为模式检测**: 通过随机化避免固定模式被识别

## 📊 性能特点

- **低资源消耗**: 轻量级活动模拟，不占用大量资源
- **高兼容性**: 支持各种学习通页面布局
- **智能恢复**: 自动处理各种异常情况
- **实时监控**: 持续监控页面状态并即时响应

## 🚀 使用方法

### 基本使用
```python
from cross_platform_course_fixed import CrossPlatformCourseAutomation, BrowserType, PlatformType

auto_course = CrossPlatformCourseAutomation(
    course_url='你的课程URL',
    browser_type=BrowserType.CHROME,
    platform_type=PlatformType.CHAOXING,  # 关键：设置为学习通
    username='你的用户名',
    password='你的密码',
    headless=False
)

# 自动启用防挂机保护
auto_course.run_simple(duration_minutes=60)
```

### 命令行运行
```bash
python cross_platform_course_fixed.py
# 按照提示选择平台类型为'chaoxing'
```

## 🔧 依赖安装
```bash
pip install selenium webdriver-manager
```

## 📈 效果预期

- ✅ 视频连续播放不间断
- ✅ 无挂机警告弹窗干扰
- ✅ 自动处理题目和恢复播放
- ✅ 智能跳转到下一个视频
- ✅ 全程无人值守运行

## 🐛 故障排除

### 常见问题
1. **视频仍然停止**: 检查防挂机日志，调整活动频率
2. **登录失败**: 确认用户名密码正确，网络连接正常
3. **题目未检测**: 检查页面布局，可能需要调整选择器

### 调试模式
启用详细日志查看防挂机活动：
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 📝 版本信息

- **文件**: `cross_platform_course_fixed.py`
- **更新日期**: 2026年3月30日
- **功能状态**: 生产就绪
- **测试状态**: 语法检查通过，功能验证完成

---

**✅ 更新完成！学习通现在具备完整的防挂机检测绕过能力，可以稳定连续播放视频课程。**