#!/bin/bash

# 跨平台刷课系统启动脚本
# 支持: macOS, Linux, Windows (通过WSL)

echo "🚀 跨平台刷课自动化系统"
echo "=" * 50

# 检查Python版本
echo "检查Python版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查操作系统
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS_NAME="Linux" ;;
    Darwin*)    OS_NAME="macOS" ;;
    CYGWIN*)    OS_NAME="Windows" ;;
    MINGW*)     OS_NAME="Windows" ;;
    *)          OS_NAME="Unknown" ;;
esac

echo "操作系统: $OS_NAME"

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 无法创建虚拟环境"
        exit 1
    fi
    echo "✅ 虚拟环境已创建"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ 无法激活虚拟环境"
    exit 1
fi
echo "✅ 虚拟环境已激活"

# 安装依赖
echo "安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi
echo "✅ 依赖已安装"

# 检查浏览器驱动
echo "检查浏览器驱动..."
echo "注意：请确保已安装以下浏览器之一："
echo "  - Chrome/Chromium"
echo "  - Firefox"
echo "  - Edge (Windows/macOS)"
echo "  - Safari (macOS)"

# 提供浏览器驱动安装建议
case "${OS_NAME}" in
    "macOS")
        echo ""
        echo "macOS 浏览器驱动安装建议："
        echo "1. Chrome: brew install --cask chromedriver"
        echo "2. Firefox: brew install geckodriver"
        echo "3. Edge: brew install --cask microsoft-edge"
        ;;
    "Linux")
        echo ""
        echo "Linux 浏览器驱动安装建议："
        echo "1. Chrome: sudo apt install chromium-chromedriver"
        echo "2. Firefox: sudo apt install firefox-geckodriver"
        ;;
    "Windows")
        echo ""
        echo "Windows 浏览器驱动安装建议："
        echo "1. 下载对应浏览器的驱动并添加到PATH"
        echo "2. 或使用 webdriver-manager 自动管理"
        ;;
esac

echo ""
echo "选择运行模式："
echo "1. 跨平台刷课系统 (推荐)"
echo "2. 原智慧树刷课脚本"
echo "3. 测试浏览器兼容性"
echo "4. 退出"
echo ""

read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo "启动跨平台刷课系统..."
        python3 cross_platform_course.py
        ;;
    2)
        echo "启动原智慧树刷课脚本..."
        python3 auto_course.py
        ;;
    3)
        echo "启动浏览器兼容性测试..."
        python3 -c "
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import platform

system = platform.system()
print(f'操作系统: {system}')

# 测试Chrome
try:
    print('测试Chrome...')
    options = ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.google.com')
    print('✅ Chrome 测试通过')
    driver.quit()
except Exception as e:
    print(f'❌ Chrome 测试失败: {e}')

# 测试Firefox
try:
    print('测试Firefox...')
    options = FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get('https://www.google.com')
    print('✅ Firefox 测试通过')
    driver.quit()
except Exception as e:
    print(f'❌ Firefox 测试失败: {e}')
"
        ;;
    4)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
echo "脚本执行完成"
echo ""
echo "提示："
echo "- 首次使用建议先运行选项3测试浏览器兼容性"
echo "- 确保网络连接稳定"
echo "- 刷课过程中请勿关闭终端窗口"