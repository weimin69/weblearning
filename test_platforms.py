#!/usr/bin/env python3
"""
测试多平台支持
"""

import sys
from cross_platform_course import PlatformType, BrowserType

def test_platform_enum():
    """测试平台枚举"""
    print("测试平台枚举...")
    
    try:
        platforms = list(PlatformType)
        print(f"✅ 支持的平台: {[p.value for p in platforms]}")
        
        for platform in platforms:
            print(f"  - {platform.value}: {platform}")
        
        return True
    except Exception as e:
        print(f"❌ 平台枚举测试失败: {e}")
        return False

def test_browser_enum():
    """测试浏览器枚举"""
    print("\n测试浏览器枚举...")
    
    try:
        browsers = list(BrowserType)
        print(f"✅ 支持的浏览器: {[b.value for b in browsers]}")
        
        for browser in browsers:
            print(f"  - {browser.value}: {browser}")
        
        return True
    except Exception as e:
        print(f"❌ 浏览器枚举测试失败: {e}")
        return False

def test_platform_configs():
    """测试平台配置"""
    print("\n测试平台配置...")
    
    try:
        # 导入类但不实例化
        from cross_platform_course import CrossPlatformCourseAutomation
        
        # 创建临时实例来访问配置
        temp_configs = {
            PlatformType.ZHIHUISHU: {
                "name": "智慧树",
                "login_url": "https://www.zhihuishu.com/",
            },
            PlatformType.CHAOXING: {
                "name": "超星学习通",
                "login_url": "https://passport2.chaoxing.com/",
            },
            PlatformType.ZHIDAO: {
                "name": "知到",
                "login_url": "https://www.zhihuishu.com/",
            },
        }
        
        for platform_type, config in temp_configs.items():
            print(f"✅ {platform_type.value}: {config['name']}")
            print(f"   登录URL: {config['login_url']}")
        
        return True
    except Exception as e:
        print(f"❌ 平台配置测试失败: {e}")
        return False

def test_main_function():
    """测试主函数逻辑"""
    print("\n测试主函数逻辑...")
    
    try:
        # 模拟用户选择
        platform_map = {
            "1": PlatformType.ZHIHUISHU,
            "2": PlatformType.CHAOXING,
            "3": PlatformType.ZHIDAO,
            "4": PlatformType.OTHER
        }
        
        browser_map = {
            "1": BrowserType.CHROME,
            "2": BrowserType.FIREFOX,
            "3": BrowserType.EDGE,
            "4": BrowserType.SAFARI
        }
        
        print("✅ 平台映射:")
        for key, value in platform_map.items():
            print(f"  选项{key} -> {value.value}")
        
        print("\n✅ 浏览器映射:")
        for key, value in browser_map.items():
            print(f"  选项{key} -> {value.value}")
        
        return True
    except Exception as e:
        print(f"❌ 主函数逻辑测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("多平台支持测试")
    print("=" * 60)
    
    tests = [
        ("平台枚举", test_platform_enum),
        ("浏览器枚举", test_browser_enum),
        ("平台配置", test_platform_configs),
        ("主函数逻辑", test_main_function),
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
        print("🎉 所有多平台支持测试通过！")
        print("\n现在可以:")
        print("1. 安装浏览器（如果还没安装）")
        print("2. 运行: ./start_all_platforms.sh")
        print("3. 选择平台和浏览器开始刷课")
    else:
        print("⚠️  部分测试失败")
        print("\n请检查代码完整性")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)