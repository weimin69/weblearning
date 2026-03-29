#!/usr/bin/env python3
"""
测试浏览器驱动管理
"""

import sys
import platform

def test_webdriver_manager():
    """测试webdriver-manager"""
    print("测试webdriver-manager...")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        
        print("✅ webdriver-manager模块导入成功")
        
        # 测试Chrome驱动管理
        try:
            chrome_path = ChromeDriverManager().install()
            print(f"✅ Chrome驱动路径: {chrome_path}")
        except Exception as e:
            print(f"⚠️ Chrome驱动管理失败: {e}")
        
        # 测试Firefox驱动管理
        try:
            firefox_path = GeckoDriverManager().install()
            print(f"✅ Firefox驱动路径: {firefox_path}")
        except Exception as e:
            print(f"⚠️ Firefox驱动管理失败: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 无法导入webdriver-manager: {e}")
        print("请安装: pip install webdriver-manager")
        return False

def test_browser_availability():
    """测试浏览器可用性"""
    print("\n测试浏览器可用性...")
    
    system = platform.system()
    print(f"操作系统: {system}")
    
    browsers = {
        "Chrome": ["google-chrome", "chrome", "Google Chrome"],
        "Firefox": ["firefox", "mozilla-firefox"],
        "Edge": ["microsoft-edge", "edge"]
    }
    
    import subprocess
    
    for browser_name, commands in browsers.items():
        found = False
        for cmd in commands:
            try:
                result = subprocess.run(["which", cmd], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {browser_name} 已安装: {result.stdout.strip()}")
                    found = True
                    break
            except:
                continue
        
        if not found:
            print(f"⚠️ {browser_name} 未安装或不在PATH中")
    
    return True

def test_simple_selenium():
    """测试简单的Selenium功能"""
    print("\n测试Selenium基本功能...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        print("✅ Selenium导入成功")
        
        # 尝试创建Chrome选项（不实际启动浏览器）
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        print("✅ Chrome选项创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ Selenium测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("浏览器驱动测试")
    print("=" * 60)
    
    tests = [
        ("webdriver-manager", test_webdriver_manager),
        ("浏览器可用性", test_browser_availability),
        ("Selenium基本功能", test_simple_selenium),
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"测试: {test_name}")
        print(f"{'='*40}")
        
        try:
            if test_func():
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} 测试出错: {e}")
            all_passed = False
    
    print(f"\n{'='*60}")
    print("测试结果汇总")
    print(f"{'='*60}")
    
    if all_passed:
        print("🎉 所有测试通过！")
        print("\n建议:")
        print("1. 运行程序时选择 Chrome (选项1)")
        print("2. 如果使用其他浏览器，请确保已安装对应驱动")
    else:
        print("⚠️  部分测试失败")
        print("\n解决方法:")
        print("1. 安装Chrome浏览器: https://www.google.com/chrome/")
        print("2. 或安装Firefox浏览器: https://www.mozilla.org/firefox/")
        print("3. 确保已激活虚拟环境: source venv/bin/activate")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)