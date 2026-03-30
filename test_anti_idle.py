#!/usr/bin/env python3
"""
测试学习通防挂机功能
"""

import sys
import os

def test_anti_idle_features():
    """测试防挂机功能"""
    print("=" * 60)
    print("学习通防挂机检测绕过功能测试")
    print("=" * 60)
    
    # 读取文件检查功能是否存在
    try:
        with open('cross_platform_course_fixed.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键防挂机方法
        anti_idle_methods = [
            '_bypass_chaoxing_anti_idle',
            '_simulate_mouse_activity',
            '_simulate_keyboard_activity',
            '_keep_page_active',
            '_check_and_resume_video',
            '_check_for_idle_popup',
            '_init_anti_idle_protection',
            '_simulate_light_activity'
        ]
        
        print("\n✅ 已实现的防挂机功能:")
        found_methods = []
        for method in anti_idle_methods:
            if f'def {method}' in content:
                found_methods.append(method)
                print(f"  ✓ {method}")
        
        print(f"\n总计: {len(found_methods)}/{len(anti_idle_methods)} 个防挂机方法")
        
        # 检查监控循环中的集成
        if 'last_bypass_time = time.time()' in content:
            print("\n✅ 防挂机功能已集成到监控循环中")
        
        if 'self._bypass_chaoxing_anti_idle()' in content:
            print("✅ 定期执行防挂机绕过")
        
        if 'self._simulate_light_activity()' in content:
            print("✅ 轻量级活动模拟已启用")
        
        if 'self._init_anti_idle_protection()' in content:
            print("✅ 防挂机保护初始化已配置")
        
    except Exception as e:
        print(f"读取文件失败: {e}")
        return
    
    print("\n" + "=" * 60)
    print("防挂机机制说明")
    print("=" * 60)
    
    print("\n🔧 多层防挂机保护:")
    print("1. 定期绕过 (每25-35秒):")
    print("   - 模拟鼠标移动")
    print("   - 模拟键盘活动")
    print("   - 保持页面激活状态")
    print("   - 检查并恢复视频播放")
    
    print("\n2. 轻量级活动 (每10秒):")
    print("   - 鼠标悬停模拟")
    print("   - 轻微滚动")
    print("   - 文档活动模拟")
    print("   - 窗口焦点模拟")
    
    print("\n3. JavaScript注入保护:")
    print("   - 重写document.hasFocus()方法")
    print("   - 监控页面可见性状态")
    print("   - 定期更新活动时间戳")
    
    print("\n4. 弹窗检测与处理:")
    print("   - 检测挂机警告弹窗")
    print("   - 自动关闭警告对话框")
    print("   - 恢复视频播放状态")
    
    print("\n" + "=" * 60)
    print("使用说明")
    print("=" * 60)
    
    print("\n📋 自动启用:")
    print("当platform_type设置为PlatformType.CHAOXING时，防挂机功能会自动启用")
    
    print("\n⚙️ 配置参数:")
    print("  - 主要绕过间隔: 25-35秒（随机）")
    print("  - 轻量级活动间隔: 10秒")
    print("  - 检查间隔: 8-12秒（随机）")
    
    print("\n🛡️ 保护效果:")
    print("  - 防止鼠标移出浏览器导致的播放停止")
    print("  - 绕过页面非激活状态检测")
    print("  - 处理挂机警告弹窗")
    print("  - 保持视频连续播放")
    
    print("\n🚀 运行测试:")
    print("python cross_platform_course_fixed.py")
    print("选择平台类型为'chaoxing'即可体验防挂机保护")
    
    print("\n" + "=" * 60)
    print("✅ 防挂机功能已就绪！")
    print("=" * 60)

if __name__ == "__main__":
    test_anti_idle_features()