#!/usr/bin/env python3
"""
最小化主脚本测试 - 直接测试课程URL访问
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

def test_course_with_main_config(course_url):
    """使用主脚本的配置测试课程URL"""
    print("=" * 60)
    print("使用主脚本配置测试课程URL")
    print("=" * 60)
    print(f"课程URL: {course_url}")
    print("=" * 60)
    
    try:
        # 使用主脚本的配置
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 添加用户代理（主脚本现在有）
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # 更多反检测措施
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        print("浏览器配置:")
        for arg in chrome_options.arguments:
            print(f"  {arg}")
        
        print("\n初始化浏览器...")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ 浏览器启动成功")
        
        # 先测试访问百度
        print("\n1. 测试访问百度...")
        driver.get("https://www.baidu.com")
        time.sleep(3)
        
        baidu_title = driver.title
        print(f"百度标题: {baidu_title}")
        
        if "百度" in baidu_title:
            print("✅ 百度访问正常")
        else:
            print("❌ 百度访问异常")
        
        # 测试访问课程URL
        print(f"\n2. 测试访问课程URL...")
        print(f"URL: {course_url}")
        
        start_time = time.time()
        driver.get(course_url)
        
        # 等待页面加载（更长的时间）
        print("等待页面加载（最长30秒）...")
        try:
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            load_time = time.time() - start_time
            print(f"✅ 页面加载完成，耗时: {load_time:.1f}秒")
        except:
            print("⚠️  页面加载超时，继续检查")
        
        # 检查页面状态
        current_url = driver.current_url
        page_title = driver.title
        page_source_length = len(driver.page_source)
        
        print(f"\n页面状态:")
        print(f"  当前URL: {current_url}")
        print(f"  页面标题: {page_title}")
        print(f"  页面大小: {page_source_length} 字符")
        
        # 检查是否重定向
        if current_url != course_url:
            print(f"⚠️  页面已重定向")
            print(f"  原始URL: {course_url}")
            print(f"  重定向到: {current_url}")
            
            # 检查是否重定向到登录页
            if any(keyword in current_url.lower() for keyword in ["login", "signin", "auth", "认证"]):
                print("⚠️  可能重定向到登录页面")
        
        # 检查页面内容
        page_text = driver.page_source.lower()
        
        # 检查常见内容
        checks = [
            ("登录页面", ["login", "signin", "登录", "登陆", "username", "password"]),
            ("视频页面", ["video", "播放", "player", "课程", "chapter"]),
            ("错误页面", ["error", "404", "not found", "无法访问", "加载失败"]),
            ("空白页面", ["<body></body>", "<html></html>", "<!-- empty -->"]),
        ]
        
        print("\n页面内容分析:")
        for check_name, keywords in checks:
            found = any(keyword in page_text for keyword in keywords)
            if found:
                print(f"  ⚠️  可能为{check_name}")
            else:
                print(f"  ✅ 不是{check_name}")
        
        # 检查是否有实际内容
        if page_source_length < 1000:
            print("\n❌ 页面内容过少，可能是空白页")
            print("可能原因:")
            print("1. 需要登录才能访问")
            print("2. 网站反爬虫机制")
            print("3. JavaScript渲染问题")
        else:
            print("\n✅ 页面有实际内容")
        
        # 截屏
        try:
            screenshot_path = "course_debug.png"
            driver.save_screenshot(screenshot_path)
            print(f"✅ 截图已保存: {screenshot_path}")
        except:
            print("⚠️  无法保存截图")
        
        # 等待用户检查
        print("\n" + "=" * 60)
        print("浏览器已打开，请检查:")
        print("1. 页面是否空白？")
        print("2. 是否需要登录？")
        print("3. 是否有验证码？")
        print("=" * 60)
        print("查看后按回车键关闭浏览器...")
        
        try:
            input()
        except:
            pass  # 非交互模式
        
        driver.quit()
        print("✅ 测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print(f"错误详情:\n{traceback.format_exc()}")
        return False

def main():
    """主函数"""
    # 获取课程URL
    if len(sys.argv) > 1:
        course_url = sys.argv[1]
    else:
        print("请输入课程URL进行测试")
        print("示例: python3 test_minimal_main.py 'https://你的课程URL'")
        return False
    
    success = test_course_with_main_config(course_url)
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    if success:
        print("✅ 测试完成")
        print("\n如果主脚本仍然空白，可能原因:")
        print("1. 主脚本有其他初始化问题")
        print("2. 页面加载时机问题")
        print("3. 需要先执行登录流程")
    else:
        print("❌ 测试失败")
        print("\n建议:")
        print("1. 手动用浏览器访问课程URL")
        print("2. 确认是否需要登录")
        print("3. 检查网络连接")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)