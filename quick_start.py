#!/usr/bin/env python3
"""
快速启动脚本
使用配置文件的简化版本
"""

import sys
import os
from cross_platform_course import CrossPlatformCourseAutomation, BrowserType

def load_config():
    """加载配置文件"""
    config_path = "config.py"
    
    if not os.path.exists(config_path):
        print("❌ 未找到配置文件 config.py")
        print("请复制 config_example.py 为 config.py 并修改配置")
        sys.exit(1)
    
    try:
        # 动态导入配置文件
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        
        return config_module.COURSE_CONFIG
    except Exception as e:
        print(f"❌ 加载配置文件失败: {e}")
        sys.exit(1)

def main():
    """主函数"""
    print("=" * 50)
    print("刷课系统 - 快速启动")
    print("=" * 50)
    
    # 加载配置
    print("加载配置文件...")
    config = load_config()
    
    # 显示配置信息
    print("\n配置信息:")
    print(f"课程URL: {config.get('course_url', '未设置')}")
    print(f"平台: {config.get('platform', 'zhihuishu')}")
    print(f"浏览器: {config.get('browser', 'chrome')}")
    print(f"无头模式: {'是' if config.get('headless', False) else '否'}")
    print(f"刷课时长: {config.get('duration_minutes', 60)}分钟")
    
    if config.get('username'):
        print(f"用户名: {config.get('username')}")
    
    print("\n" + "=" * 50)
    
    # 确认开始
    confirm = input("确认开始刷课？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    # 映射平台类型
    platform_map = {
        "zhihuishu": PlatformType.ZHIHUISHU,
        "chaoxing": PlatformType.CHAOXING,
        "zhidao": PlatformType.ZHIDAO,
        "other": PlatformType.OTHER,
    }
    
    platform_type = platform_map.get(config.get('platform', 'zhihuishu'), PlatformType.ZHIHUISHU)
    
    # 映射浏览器类型
    browser_map = {
        "chrome": BrowserType.CHROME,
        "firefox": BrowserType.FIREFOX,
        "edge": BrowserType.EDGE,
        "safari": BrowserType.SAFARI,
    }
    
    browser_type = browser_map.get(config.get('browser', 'chrome'), BrowserType.CHROME)
    
    # 创建并运行自动化工具
    auto_course = CrossPlatformCourseAutomation(
        course_url=config['course_url'],
        browser_type=browser_type,
        platform_type=platform_type,
        username=config.get('username'),
        password=config.get('password'),
        headless=config.get('headless', False)
    )
    
    try:
        auto_course.run(config.get('duration_minutes', 60))
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"程序运行出错: {e}")
    finally:
        auto_course.cleanup()

if __name__ == "__main__":
    main()