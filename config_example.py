#!/usr/bin/env python3
"""
刷课系统配置文件示例
复制此文件为 config.py 并修改配置
"""

# 课程配置
COURSE_CONFIG = {
    # 课程页面URL (必填)
    "course_url": "https://www.zhihuishu.com/你的课程页面",
    
    # 平台选择
    "platform": "zhihuishu",  # zhihuishu, chaoxing, zhidao, other
    
    # 登录信息 (可选，如果不填会提示手动登录)
    "username": "你的用户名",
    "password": "你的密码",
    
    # 刷课时长 (分钟)
    "duration_minutes": 60,
    
    # 浏览器配置
    "browser": "chrome",  # chrome, firefox, edge, safari
    "headless": False,    # 是否使用无头模式
    
    # 高级配置
    "check_interval": 15,     # 检查题目间隔(秒)
    "video_check_interval": 10,  # 检查视频结束间隔(秒)
    "status_interval": 30,    # 状态报告间隔(秒)
}

# 自定义选择器 (如果默认选择器不工作，可以在这里添加)
CUSTOM_SELECTORS = {
    # 播放按钮选择器
    "play_buttons": [
        ".custom-play-btn",  # 添加自定义选择器
        "#video-play-button",
    ],
    
    # 题目弹窗选择器
    "question_popups": [
        ".custom-question-popup",
        "#exam-dialog",
    ],
    
    # 答案选项选择器
    "answer_options": [
        ".custom-option",
        ".quiz-choice",
    ],
    
    # 下一个视频按钮选择器
    "next_video_buttons": [
        ".custom-next-btn",
        "#next-video",
    ],
    
    # 关闭按钮选择器
    "close_buttons": [
        ".custom-close-btn",
        "#modal-close",
    ],
}

# 平台特定配置
PLATFORM_CONFIG = {
    "windows": {
        "chrome_driver_path": "chromedriver.exe",
        "firefox_driver_path": "geckodriver.exe",
        "edge_driver_path": "msedgedriver.exe",
    },
    "darwin": {  # macOS
        "chrome_driver_path": "/usr/local/bin/chromedriver",
        "firefox_driver_path": "/usr/local/bin/geckodriver",
        "edge_driver_path": "/usr/local/bin/msedgedriver",
    },
    "linux": {
        "chrome_driver_path": "/usr/bin/chromedriver",
        "firefox_driver_path": "/usr/bin/geckodriver",
        "edge_driver_path": "/usr/bin/msedgedriver",
    }
}