#!/usr/bin/env python3
"""
测试页面加载问题
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def test_basic_page_load():
    """测试基本页面加载"""
    print("测试基本页面加载...")
    
    try:
        # 创建Chrome选项
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        
        # 使用webdriver-manager
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ 浏览器启动成功")
        
        # 测试访问百度（国内可访问）
        test_url = "https://www.baidu.com"
        print(f"访问测试页面: {test_url}")
        
        driver.get(test_url)
        
        # 等待页面加载
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("✅ 页面加载完成")
            
            # 检查页面信息
            current_url = driver.current_url
            page_title = driver.title
            page_source_length = len(driver.page_source)
            
            print(f"  当前URL: {current_url}")
            print(f"  页面标题: {page_title}")
            print(f"  页面大小: {page_source_length} 字符")
            
            if page_source_length < 1000:
                print("⚠️  页面内容过少，可能加载失败")
            else:
                print("✅ 页面内容正常")
            
            # 检查是否有百度特定元素
            try:
                search_box = driver.find_element("id", "kw")
                print("✅ 找到百度搜索框")
            except:
                print("⚠️  未找到百度搜索框，页面可能不正常")
            
        except TimeoutException:
            print("❌ 页面加载超时")
        
        # 测试访问智慧树
        print("\n测试访问智慧树...")
        zhihuishu_url = "https://www.zhihuishu.com"
        print(f"访问: {zhihuishu_url}")
        
        driver.get(zhihuishu_url)
        
        try:
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("✅ 智慧树页面加载完成")
            
            current_url = driver.current_url
            page_title = driver.title
            page_source_length = len(driver.page_source)
            
            print(f"  当前URL: {current_url}")
            print(f"  页面标题: {page_title}")
            print(f"  页面大小: {page_source_length} 字符")
            
            # 检查页面内容
            page_text = driver.page_source.lower()
            if "zhihuishu" in page_text or "智慧树" in page_text:
                print("✅ 页面包含智慧树相关关键词")
            else:
                print("⚠️  页面可能不是智慧树官网")
            
        except TimeoutException:
            print("❌ 智慧树页面加载超时")
            print("可能原因:")
            print("1. 网络连接问题")
            print("2. 网站访问限制")
            print("3. DNS解析问题")
        
        # 关闭浏览器
        driver.quit()
        print("\n✅ 测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_network_connectivity():
    """测试网络连接"""
    print("\n测试网络连接...")
    
    import subprocess
    import socket
    
    test_hosts = [
        ("百度", "www.baidu.com"),
        ("智慧树", "www.zhihuishu.com"),
        ("超星", "passport2.chaoxing.com"),
        ("Google DNS", "8.8.8.8")
    ]
    
    all_connected = True
    
    for name, host in test_hosts:
        try:
            # 尝试ping（macOS/Linux）
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "2", host],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ {name} ({host}) - 网络可达")
            else:
                print(f"❌ {name} ({host}) - 网络不可达")
                all_connected = False
                
        except Exception as e:
            print(f"⚠️  {name} ({host}) - 测试失败: {e}")
            all_connected = False
    
    return all_connected

def test_dns_resolution():
    """测试DNS解析"""
    print("\n测试DNS解析...")
    
    import socket
    
    test_domains = [
        ("百度", "www.baidu.com"),
        ("智慧树", "www.zhihuishu.com"),
        ("超星", "passport2.chaoxing.com")
    ]
    
    all_resolved = True
    
    for name, domain in test_domains:
        try:
            ip_address = socket.gethostbyname(domain)
            print(f"✅ {name} ({domain}) - 解析为: {ip_address}")
        except socket.gaierror:
            print(f"❌ {name} ({domain}) - DNS解析失败")
            all_resolved = False
        except Exception as e:
            print(f"⚠️  {name} ({domain}) - 解析错误: {e}")
            all_resolved = False
    
    return all_resolved

def test_browser_debug_mode():
    """测试浏览器调试模式"""
    print("\n测试浏览器调试模式...")
    
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--log-level=0")  # 禁用日志
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        # 添加详细日志
        chrome_options.add_argument("--verbose")
        chrome_options.add_argument("--v=1")
        
        service = ChromeService(
            ChromeDriverManager().install(),
            service_args=["--verbose", "--log-path=chrome.log"]
        )
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ 调试模式浏览器启动成功")
        print("浏览器日志将保存到: chrome.log")
        
        # 快速测试
        driver.get("https://www.baidu.com")
        time.sleep(2)
        
        page_title = driver.title
        print(f"测试页面标题: {page_title}")
        
        driver.quit()
        print("✅ 调试测试完成")
        
        # 检查日志文件
        try:
            with open("chrome.log", "r") as f:
                log_content = f.read()
                if "error" in log_content.lower():
                    print("⚠️  浏览器日志中包含错误")
                else:
                    print("✅ 浏览器日志正常")
        except:
            print("ℹ️  未找到浏览器日志文件")
        
        return True
        
    except Exception as e:
        print(f"❌ 调试模式测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("页面加载问题诊断工具")
    print("=" * 60)
    
    tests = [
        ("网络连接", test_network_connectivity),
        ("DNS解析", test_dns_resolution),
        ("基本页面加载", test_basic_page_load),
        ("浏览器调试", test_browser_debug_mode),
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
    print("诊断结果汇总")
    print(f"{'='*60}")
    
    if all_passed:
        print("🎉 所有测试通过！网络和浏览器正常")
        print("\n如果脚本仍然打开空白页面，可能是:")
        print("1. 目标网站访问限制")
        print("2. 需要验证码或人工验证")
        print("3. 网站反爬虫机制")
    else:
        print("⚠️  发现一些问题")
        print("\n常见问题解决:")
        print("1. 检查网络连接")
        print("2. 检查DNS设置")
        print("3. 尝试使用其他浏览器")
        print("4. 检查防火墙设置")
        print("5. 尝试使用VPN（如果访问国外网站）")
    
    print("\n建议:")
    print("1. 手动用浏览器访问目标网站，确认可以正常打开")
    print("2. 检查是否有验证码需要手动输入")
    print("3. 尝试使用无头模式测试")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)