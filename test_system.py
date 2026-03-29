#!/usr/bin/env python3
"""
刷课系统功能测试
测试跨平台刷课系统的核心功能
"""

import sys
import os

def test_imports():
    """测试必要的导入"""
    print("测试Python模块导入...")
    
    try:
        import selenium
        print("✅ selenium 导入成功")
    except ImportError:
        print("❌ selenium 导入失败")
        return False
    
    try:
        from selenium import webdriver
        print("✅ webdriver 导入成功")
    except ImportError:
        print("❌ webdriver 导入失败")
        return False
    
    return True

def test_config_files():
    """测试配置文件"""
    print("\n测试配置文件...")
    
    required_files = [
        "cross_platform_course.py",
        "requirements.txt",
        "config_example.py",
        "README.md"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} 存在")
        else:
            print(f"❌ {file} 不存在")
            all_exist = False
    
    return all_exist

def test_script_permissions():
    """测试脚本权限"""
    print("\n测试脚本权限...")
    
    scripts = ["start_all_platforms.sh", "start.sh"]
    
    for script in scripts:
        if os.path.exists(script):
            if os.access(script, os.X_OK):
                print(f"✅ {script} 有执行权限")
            else:
                print(f"⚠️ {script} 无执行权限，运行: chmod +x {script}")
        else:
            print(f"ℹ️ {script} 不存在")
    
    return True

def test_python_version():
    """测试Python版本"""
    print("\n测试Python版本...")
    
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python版本符合要求 (>= 3.8)")
        return True
    else:
        print("❌ Python版本过低，需要3.8+")
        return False

def test_system_info():
    """测试系统信息"""
    print("\n系统信息:")
    
    import platform
    system = platform.system()
    release = platform.release()
    machine = platform.machine()
    
    print(f"操作系统: {system} {release}")
    print(f"架构: {machine}")
    
    # 检查浏览器驱动
    print("\n浏览器驱动检查:")
    
    browsers = ["chrome", "firefox", "edge"]
    for browser in browsers:
        # 检查常见驱动路径
        paths = []
        if system == "Darwin":  # macOS
            paths = [
                f"/usr/local/bin/{browser}driver",
                f"/opt/homebrew/bin/{browser}driver"
            ]
        elif system == "Linux":
            paths = [
                f"/usr/bin/{browser}driver",
                f"/usr/local/bin/{browser}driver"
            ]
        elif system == "Windows":
            paths = [
                f"{browser}driver.exe",
                f"C:\\Program Files\\{browser.capitalize()}\\{browser}driver.exe"
            ]
        
        found = False
        for path in paths:
            if os.path.exists(path):
                print(f"✅ {browser}驱动: {path}")
                found = True
                break
        
        if not found:
            print(f"⚠️ {browser}驱动未找到，可能需要安装")
    
    return True

def test_cross_platform_class():
    """测试跨平台类结构"""
    print("\n测试跨平台类结构...")
    
    try:
        # 尝试导入类但不实例化
        from cross_platform_course import CrossPlatformCourseAutomation, BrowserType
        
        print("✅ CrossPlatformCourseAutomation 类导入成功")
        print("✅ BrowserType 枚举导入成功")
        
        # 检查类的方法
        methods = [
            "login", "navigate_to_course", "play_video",
            "check_for_questions", "answer_question", "go_to_next_video",
            "close_popup", "monitor_course", "run", "cleanup"
        ]
        
        for method in methods:
            if hasattr(CrossPlatformCourseAutomation, method):
                print(f"✅ 方法 {method} 存在")
            else:
                print(f"❌ 方法 {method} 不存在")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入跨平台类失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("刷课系统功能测试")
    print("=" * 60)
    
    tests = [
        ("Python版本", test_python_version),
        ("模块导入", test_imports),
        ("配置文件", test_config_files),
        ("脚本权限", test_script_permissions),
        ("系统信息", test_system_info),
        ("类结构", test_cross_platform_class),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"测试: {test_name}")
        print(f"{'='*40}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 测试 {test_name} 出错: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print(f"\n{'='*60}")
    print("测试结果汇总")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统可以正常使用。")
        print("\n下一步:")
        print("1. 运行: chmod +x start_all_platforms.sh")
        print("2. 运行: ./start_all_platforms.sh")
        print("3. 选择选项1开始刷课")
    else:
        print(f"\n⚠️  {total - passed} 项测试失败，请检查问题。")
        print("\n常见问题解决:")
        print("1. 安装缺失的依赖: pip install -r requirements.txt")
        print("2. 添加脚本执行权限: chmod +x *.sh")
        print("3. 安装浏览器驱动（参考README_FULL.md）")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)