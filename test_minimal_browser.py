#!/usr/bin/env python3
"""
最小化浏览器测试 - 测试主脚本的浏览器初始化
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def test_simple_browser():
    """测试最简单的浏览器初始化"""
    print("测试最简单的浏览器初始化...")
    
    try:
        # 最简单的Chrome选项
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        
        # 使用webdriver-manager
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ 浏览器启动成功")
        
        # 测试访问百度
        test_url = "https://www.baidu.com"
        print(f"访问测试页面: {test_url}")
        
        driver.get(test_url)
        
        # 等待页面加载
        time.sleep(3)
        
        # 检查页面信息
        current_url = driver.current_url
        page_title = driver.title
        
        print(f"  当前URL: {current_url}")
        print(f"  页面标题: {page_title}")
        
        if "百度" in page_title:
            print("✅ 页面加载正常")
        else:
            print("⚠️  页面标题异常")
        
        # 保持浏览器打开以便检查
        print("\n浏览器将保持打开10秒...")
        time.sleep(10)
        
        driver.quit()
        print("✅ 测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_main_script_browser():
    """测试主脚本中的浏览器初始化方法"""
    print("\n" + "="*60)
    print("测试主脚本的浏览器初始化...")
    
    # 模拟主脚本的浏览器初始化
    try:
        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from webdriver_manager.chrome import ChromeDriverManager
        
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 添加用户代理
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # 更多反检测措施
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        # 使用webdriver-manager自动管理驱动
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ 主脚本浏览器启动成功")
        
        # 测试访问百度
        test_url = "https://www.baidu.com"
        print(f"访问测试页面: {test_url}")
        
        driver.get(test_url)
        
        # 等待页面加载
        time.sleep(3)
        
        # 检查页面信息
        current_url = driver.current_url
        page_title = driver.title
        
        print(f"  当前URL: {current_url}")
        print(f"  页面标题: {page_title}")
        
        if "百度" in page_title:
            print("✅ 主脚本浏览器页面加载正常")
        else:
            print("⚠️  主脚本浏览器页面标题异常")
        
        # 保持浏览器打开以便检查
        print("\n浏览器将保持打开10秒...")
        time.sleep(10)
        
        driver.quit()
        print("✅ 主脚本浏览器测试完成")
        
    except Exception as e:
        print(f"❌ 主脚本浏览器测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("="*60)
    print("最小化浏览器测试")
    print("="*60)
    
    # 测试1: 最简单的浏览器
    test_simple_browser()
    
    # 测试2: 主脚本的浏览器
    test_main_script_browser()