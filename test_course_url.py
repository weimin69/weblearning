#!/usr/bin/env python3
"""
测试课程URL访问
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

def test_course_url(course_url):
    """测试特定课程URL"""
    print(f"测试课程URL: {course_url}")
    
    try:
        # 创建Chrome选项
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        
        # 添加用户代理，模拟真实浏览器
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # 禁用自动化控制标志
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ 浏览器启动成功")
        
        # 访问课程URL
        print(f"访问: {course_url}")
        driver.get(course_url)
        
        # 等待页面加载
        try:
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("✅ 页面加载完成")
        except:
            print("⚠️  页面加载超时，继续检查")
        
        # 检查页面信息
        current_url = driver.current_url
        page_title = driver.title
        page_source_length = len(driver.page_source)
        
        print(f"\n页面信息:")
        print(f"  当前URL: {current_url}")
        print(f"  页面标题: {page_title}")
        print(f"  页面大小: {page_source_length} 字符")
        
        # 检查是否重定向
        if current_url != course_url:
            print(f"⚠️  页面已重定向")
            print(f"  原始URL: {course_url}")
            print(f"  重定向到: {current_url}")
        
        # 检查页面内容
        page_text = driver.page_source.lower()
        
        # 检查常见关键词
        keywords = {
            "登录": ["login", "signin", "登录", "登陆"],
            "视频": ["video", "播放", "study", "学习"],
            "课程": ["course", "lesson", "课程", "章节"],
            "错误": ["error", "404", "not found", "无法访问", "加载失败"]
        }
        
        print("\n页面内容分析:")
        for category, words in keywords.items():
            found_words = [word for word in words if word in page_text]
            if found_words:
                print(f"  ✅ 包含{category}关键词: {', '.join(found_words[:3])}")
            else:
                print(f"  ❌ 未找到{category}关键词")
        
        # 检查是否有iframe
        iframes = driver.find_elements("tag name", "iframe")
        if iframes:
            print(f"⚠️  页面包含 {len(iframes)} 个iframe，可能影响自动化")
        
        # 检查是否有视频元素
        videos = driver.find_elements("tag name", "video")
        if videos:
            print(f"✅ 找到 {len(videos)} 个视频元素")
        else:
            print("❌ 未找到视频元素")
        
        # 截屏保存
        try:
            screenshot_path = "course_page.png"
            driver.save_screenshot(screenshot_path)
            print(f"✅ 页面截图已保存: {screenshot_path}")
        except:
            print("⚠️  无法保存截图")
        
        # 等待用户查看
        print("\n浏览器已打开，请查看页面内容...")
        print("按回车键关闭浏览器并继续")
        input()
        
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
    print("=" * 60)
    print("课程URL访问测试")
    print("=" * 60)
    
    # 获取课程URL
    if len(sys.argv) > 1:
        course_url = sys.argv[1]
    else:
        course_url = input("请输入课程URL: ").strip()
    
    if not course_url:
        print("❌ 未提供课程URL")
        return False
    
    print(f"\n测试课程URL: {course_url}")
    print("=" * 60)
    
    success = test_course_url(course_url)
    
    print(f"\n{'='*60}")
    print("测试结果")
    print(f"{'='*60}")
    
    if success:
        print("✅ 课程URL测试完成")
        print("\n建议:")
        print("1. 如果页面需要登录，请先手动登录")
        print("2. 如果页面有验证码，需要手动处理")
        print("3. 确认页面包含视频播放器")
    else:
        print("❌ 课程URL测试失败")
        print("\n可能原因:")
        print("1. URL错误或无效")
        print("2. 需要登录才能访问")
        print("3. 网络或网站限制")
        print("4. 反爬虫机制")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)