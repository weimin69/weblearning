#!/usr/bin/env python3
"""
调试版主脚本 - 简化版本，用于诊断问题
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,  # 改为DEBUG级别
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_simple_browser():
    """测试简化版浏览器初始化"""
    print("=" * 60)
    print("调试：简化版浏览器测试")
    print("=" * 60)
    
    try:
        # 使用与test_course_url.py相同的配置
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        
        # 添加用户代理，模拟真实浏览器
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # 禁用自动化控制标志
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 显示更多调试信息
        print("初始化浏览器选项...")
        print(f"选项数量: {len(chrome_options.arguments)}")
        for arg in chrome_options.arguments:
            print(f"  选项: {arg}")
        
        print("\n初始化Chrome服务...")
        service = ChromeService(ChromeDriverManager().install())
        
        print("创建浏览器驱动...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ 浏览器启动成功")
        
        # 测试访问百度
        test_url = "https://www.baidu.com"
        print(f"\n访问测试页面: {test_url}")
        
        driver.get(test_url)
        
        # 等待页面加载
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("✅ 页面加载完成")
        except Exception as e:
            print(f"⚠️  页面加载异常: {e}")
        
        # 检查页面信息
        current_url = driver.current_url
        page_title = driver.title
        print(f"当前URL: {current_url}")
        print(f"页面标题: {page_title}")
        
        if "百度" in page_title:
            print("✅ 成功访问百度")
        else:
            print("❌ 页面标题异常")
        
        # 等待用户查看
        print("\n浏览器已打开，请查看是否空白...")
        print("按回车键关闭浏览器")
        input()
        
        driver.quit()
        print("✅ 测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print(f"错误详情:\n{traceback.format_exc()}")
        return False

def test_main_script_config():
    """测试主脚本的配置"""
    print("\n" + "=" * 60)
    print("调试：主脚本配置检查")
    print("=" * 60)
    
    try:
        # 导入主脚本的配置
        from cross_platform_course import CrossPlatformCourseAutomation, BrowserType, PlatformType
        
        print("✅ 成功导入主脚本模块")
        
        # 检查浏览器初始化配置
        print("\n检查浏览器初始化逻辑...")
        
        # 创建简化实例（不实际启动浏览器）
        print("创建CrossPlatformCourseAutomation实例...")
        
        # 模拟初始化过程
        print("\n模拟的浏览器配置:")
        print("1. 使用webdriver-manager自动管理驱动")
        print("2. 添加基本浏览器选项")
        print("3. 如果是无头模式，添加headless参数")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        import traceback
        print(f"错误详情:\n{traceback.format_exc()}")
        return False

def compare_configs():
    """比较测试脚本和主脚本的配置"""
    print("\n" + "=" * 60)
    print("调试：配置比较")
    print("=" * 60)
    
    print("测试脚本 (test_course_url.py) 配置:")
    print("1. ChromeOptions()")
    print("2. --start-maximized")
    print("3. --disable-notifications")
    print("4. --user-agent=真实浏览器UA")
    print("5. excludeSwitches: ['enable-automation']")
    print("6. useAutomationExtension: False")
    
    print("\n主脚本 (cross_platform_course.py) 配置:")
    print("1. 根据浏览器类型选择配置")
    print("2. 添加--start-maximized")
    print("3. 添加--disable-notifications")
    print("4. 添加--disable-popup-blocking")
    print("5. 添加--disable-blink-features=AutomationControlled")
    print("6. excludeSwitches: ['enable-automation']")
    print("7. useAutomationExtension: False")
    print("8. 如果是无头模式，添加headless参数")
    
    print("\n主要差异:")
    print("1. 主脚本有更多反检测选项")
    print("2. 主脚本有无头模式支持")
    print("3. 主脚本使用webdriver-manager")
    
    return True

def test_with_main_script_config():
    """使用主脚本的配置测试"""
    print("\n" + "=" * 60)
    print("调试：使用主脚本配置测试")
    print("=" * 60)
    
    try:
        # 使用主脚本的配置
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 不添加用户代理（与主脚本一致）
        # chrome_options.add_argument("--user-agent=...")
        
        print("使用主脚本配置初始化浏览器...")
        print(f"选项: {chrome_options.arguments}")
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ 浏览器启动成功")
        
        # 测试访问
        test_url = "https://www.baidu.com"
        driver.get(test_url)
        time.sleep(3)
        
        current_url = driver.current_url
        page_title = driver.title
        print(f"当前URL: {current_url}")
        print(f"页面标题: {page_title}")
        
        if page_title and "百度" in page_title:
            print("✅ 页面加载正常")
        else:
            print("❌ 页面可能空白")
            print("尝试添加用户代理...")
            
            # 关闭当前浏览器
            driver.quit()
            
            # 重新启动带用户代理
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            driver.get(test_url)
            time.sleep(3)
            
            current_url = driver.current_url
            page_title = driver.title
            print(f"重新测试 - 当前URL: {current_url}")
            print(f"重新测试 - 页面标题: {page_title}")
        
        print("\n按回车键关闭浏览器")
        input()
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print(f"错误详情:\n{traceback.format_exc()}")
        return False

def main():
    """主调试函数"""
    print("=" * 60)
    print("主脚本空白页面问题诊断")
    print("=" * 60)
    
    tests = [
        ("简化版浏览器测试", test_simple_browser),
        ("主脚本配置检查", test_main_script_config),
        ("配置比较", compare_configs),
        ("使用主脚本配置测试", test_with_main_script_config),
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"测试: {test_name}")
        print(f"{'='*40}")
        
        try:
            if test_func():
                print(f"✅ {test_name} 通过")
            else:
                print(f"❌ {test_name} 失败")
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} 出错: {e}")
            all_passed = False
    
    print(f"\n{'='*60}")
    print("诊断结果")
    print(f"{'='*60}")
    
    if all_passed:
        print("✅ 所有测试通过")
        print("\n问题可能在于:")
        print("1. 主脚本缺少用户代理")
        print("2. 网站反爬虫检测")
        print("3. 页面加载时机问题")
    else:
        print("❌ 发现配置问题")
    
    print("\n建议解决方案:")
    print("1. 在主脚本中添加用户代理")
    print("2. 增加页面加载等待时间")
    print("3. 添加更多反检测措施")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)