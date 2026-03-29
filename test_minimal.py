#!/usr/bin/env python3
"""
最小化测试 - 不实际启动浏览器
"""

import sys
from cross_platform_course import CrossPlatformCourseAutomation, BrowserType

def test_class_structure():
    """测试类结构"""
    print("测试类结构...")
    
    try:
        # 测试导入
        print("✅ 类导入成功")
        
        # 测试枚举
        print(f"✅ BrowserType枚举: {list(BrowserType)}")
        
        # 测试方法
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
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 类结构测试失败: {e}")
        return False

def test_config_parsing():
    """测试配置解析"""
    print("\n测试配置解析...")
    
    try:
        # 测试配置示例
        with open("config_example.py", "r") as f:
            content = f.read()
            if "COURSE_CONFIG" in content:
                print("✅ 配置文件结构正确")
                return True
            else:
                print("❌ 配置文件缺少COURSE_CONFIG")
                return False
    except Exception as e:
        print(f"❌ 配置解析测试失败: {e}")
        return False

def test_quick_start():
    """测试快速启动脚本"""
    print("\n测试快速启动脚本...")
    
    try:
        with open("quick_start.py", "r") as f:
            content = f.read()
            if "load_config" in content and "main" in content:
                print("✅ 快速启动脚本结构正确")
                return True
            else:
                print("❌ 快速启动脚本结构不完整")
                return False
    except Exception as e:
        print(f"❌ 快速启动脚本测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("最小化功能测试")
    print("=" * 60)
    print("注意：此测试不实际启动浏览器")
    print("=" * 60)
    
    tests = [
        ("类结构", test_class_structure),
        ("配置解析", test_config_parsing),
        ("快速启动", test_quick_start),
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
        print("🎉 所有代码结构测试通过！")
        print("\n下一步:")
        print("1. 安装Chrome浏览器（推荐）")
        print("2. 或安装Firefox浏览器")
        print("3. 然后运行: ./start_all_platforms.sh")
    else:
        print("⚠️  代码结构测试失败")
        print("\n请检查代码完整性")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)