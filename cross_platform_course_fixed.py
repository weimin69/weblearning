#!/usr/bin/env python3
"""
修复版跨平台刷课系统 - 解决空白页面问题
"""

import time
import random
import logging
import platform
import sys
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BrowserType(Enum):
    """支持的浏览器类型"""
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"

class PlatformType(Enum):
    """支持的刷课平台"""
    ZHIHUISHU = "zhihuishu"      # 智慧树
    CHAOXING = "chaoxing"        # 超星学习通
    ZHIDAO = "zhidao"            # 知到
    OTHER = "other"              # 其他平台

class CrossPlatformCourseAutomation:
    def __init__(self, course_url, browser_type=BrowserType.CHROME, 
                 platform_type=PlatformType.ZHIHUISHU,
                 username=None, password=None, headless=False):
        """
        初始化跨平台刷课工具
        
        Args:
            course_url: 课程页面URL
            browser_type: 浏览器类型 (chrome, firefox, edge, safari)
            platform_type: 平台类型 (zhihuishu, chaoxing, zhidao, other)
            username: 用户名（可选）
            password: 密码（可选）
            headless: 是否使用无头模式
        """
        self.course_url = course_url
        self.username = username
        self.password = password
        self.browser_type = browser_type
        self.platform_type = platform_type
        self.headless = headless
        
        # 平台配置
        self.platform_configs = {
            PlatformType.ZHIHUISHU: {
                "name": "智慧树",
                "login_url": "https://www.zhihuishu.com/",
                "home_url": "https://www.zhihuishu.com/",
                "selectors": {
                    "login_btn": ".login-btn",
                    "username_input": "input[name='username']",
                    "password_input": "input[name='password']",
                    "submit_btn": ".submit-btn"
                }
            },
            PlatformType.CHAOXING: {
                "name": "超星学习通",
                "login_url": "https://passport2.chaoxing.com/",
                "home_url": "https://i.chaoxing.com/",
                "selectors": {
                    "login_btn": ".login-btn",
                    "username_input": "input[name='uname']",
                    "password_input": "input[name='password']",
                    "submit_btn": ".login-btn"
                }
            },
            PlatformType.ZHIDAO: {
                "name": "知到",
                "login_url": "https://www.zhihuishu.com/",
                "home_url": "https://www.zhihuishu.com/",
                "selectors": {
                    "login_btn": ".login-btn",
                    "username_input": "input[name='username']",
                    "password_input": "input[name='password']",
                    "submit_btn": ".submit-btn"
                }
            },
            PlatformType.OTHER: {
                "name": "其他平台",
                "login_url": None,
                "home_url": None,
                "selectors": {}
            }
        }
        
        # 初始化浏览器驱动
        self.driver = self._init_browser_driver_simple()
        self.wait = WebDriverWait(self.driver, 20)  # 增加等待时间
        self.action = ActionChains(self.driver)
        
        logger.info(f"{browser_type.value.capitalize()}浏览器已启动")
        logger.info(f"目标平台: {self.platform_configs[platform_type]['name']}")
    
    def _init_browser_driver_simple(self):
        """简化的浏览器初始化，避免空白页面问题"""
        system = platform.system().lower()
        
        try:
            if self.browser_type == BrowserType.CHROME:
                from selenium.webdriver.chrome.service import Service as ChromeService
                from selenium.webdriver.chrome.options import Options as ChromeOptions
                from webdriver_manager.chrome import ChromeDriverManager
                
                chrome_options = ChromeOptions()
                
                # 基本选项
                chrome_options.add_argument("--start-maximized")
                chrome_options.add_argument("--disable-notifications")
                chrome_options.add_argument("--disable-popup-blocking")
                
                # 反检测措施
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                # 用户代理（重要！）
                chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                
                # 性能优化
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                
                if self.headless:
                    chrome_options.add_argument("--headless")
                    chrome_options.add_argument("--window-size=1920,1080")
                
                # 使用webdriver-manager
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # 执行JavaScript来隐藏webdriver特征
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                return driver
            
            elif self.browser_type == BrowserType.FIREFOX:
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                from webdriver_manager.firefox import GeckoDriverManager
                
                firefox_options = FirefoxOptions()
                firefox_options.add_argument("--start-maximized")
                firefox_options.set_preference("dom.webnotifications.enabled", False)
                
                # 用户代理
                firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                
                # 反检测
                firefox_options.set_preference("dom.webdriver.enabled", False)
                firefox_options.set_preference("useAutomationExtension", False)
                
                if self.headless:
                    firefox_options.add_argument("--headless")
                
                service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=firefox_options)
            
            else:
                # 默认使用Chrome
                logger.warning(f"{self.browser_type.value}浏览器可能有问题，使用Chrome代替")
                return self._init_browser_driver_simple()
                
        except Exception as e:
            logger.error(f"初始化浏览器驱动失败: {e}")
            raise
    
    def wait_for_page_load(self, timeout=30):
        """等待页面完全加载"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logger.info("页面加载完成")
            return True
        except TimeoutException:
            logger.warning(f"页面加载超时 ({timeout}秒)")
            return False
    
    def login(self):
        """登录平台（如果需要）"""
        if not self.username or not self.password:
            logger.info("未提供登录凭据，请手动登录")
            platform_name = self.platform_configs[self.platform_type]["name"]
            print(f"\n请手动登录 {platform_name} 平台")
            print("登录完成后按回车键继续...")
            input()
            return
        
        platform_config = self.platform_configs[self.platform_type]
        platform_name = platform_config["name"]
        login_url = platform_config["login_url"]
        
        if not login_url:
            logger.info(f"{platform_name} 平台需要手动登录")
            input("请手动登录，完成后按回车键继续...")
            return
        
        logger.info(f"正在登录 {platform_name} 平台...")
        try:
            # 访问登录页面
            logger.info(f"访问登录页面: {login_url}")
            self.driver.get(login_url)
            
            # 等待页面加载
            self.wait_for_page_load(15)
            
            # 检查当前页面
            current_url = self.driver.current_url
            page_title = self.driver.title
            logger.info(f"当前URL: {current_url}")
            logger.info(f"页面标题: {page_title}")
            
            # 如果已经登录或重定向，直接返回
            if "login" not in current_url.lower() and "signin" not in current_url.lower():
                logger.info("可能已自动登录或已在登录状态")
                return
            
            # 尝试登录（简化版）
            time.sleep(2)
            logger.info("尝试自动登录...")
            
            # 这里可以添加具体的登录逻辑
            # 由于不同平台登录方式不同，建议使用手动登录
            
            logger.info("自动登录可能失败，请手动登录")
            input("请手动登录，完成后按回车键继续...")
            
        except Exception as e:
            logger.error(f"登录过程中出错: {e}")
            logger.info("请手动登录")
            input("请手动登录，完成后按回车键继续...")
    
    def navigate_to_course_simple(self):
        """简化的课程页面导航"""
        logger.info(f"正在访问课程页面: {self.course_url}")
        
        try:
            # 直接访问课程URL
            self.driver.get(self.course_url)
            
            # 等待页面加载
            if not self.wait_for_page_load(20):
                logger.warning("页面加载较慢，继续尝试...")
            
            # 检查页面状态
            current_url = self.driver.current_url
            page_title = self.driver.title
            page_source_length = len(self.driver.page_source)
            
            logger.info(f"页面状态:")
            logger.info(f"  当前URL: {current_url}")
            logger.info(f"  页面标题: {page_title}")
            logger.info(f"  页面大小: {page_source_length} 字符")
            
            if page_source_length < 1000:
                logger.warning("页面内容过少，可能是空白页或需要登录")
                print("\n⚠️  页面可能空白，请检查:")
                print("1. 是否需要登录？")
                print("2. 课程URL是否正确？")
                print("3. 网络是否正常？")
                
                # 截屏
                try:
                    self.driver.save_screenshot("course_page_debug.png")
                    logger.info("页面截图已保存: course_page_debug.png")
                except:
                    pass
            
            return True
            
        except Exception as e:
            logger.error(f"访问课程页面失败: {e}")
            return False
    
    def run_simple(self, duration_minutes=60, manual_mode=True):
        """简化的运行方法"""
        print("=" * 60)
        print("修复版刷课系统 - 简化模式")
        print("=" * 60)
        
        try:
            # 1. 登录（如果需要）
            self.login()
            
            # 2. 导航到课程
            if not self.navigate_to_course_simple():
                print("\n❌ 课程页面访问失败")
                print("请检查:")
                print(f"1. 课程URL: {self.course_url}")
                print("2. 是否已登录平台")
                print("3. 网络连接")
                return
            
            # 3. 手动模式提示
            if manual_mode:
                print("\n" + "=" * 60)
                print("手动模式说明:")
                print("1. 请手动选择要刷的视频")
                print("2. 手动点击播放按钮")
                print("3. 脚本将自动处理题目和播放下一个视频")
                print("=" * 60)
                input("\n准备好后按回车键开始自动化监控...")
            
            # 4. 开始简单监控
            self.monitor_simple(duration_minutes)
            
        except KeyboardInterrupt:
            print("\n用户中断程序")
        except Exception as e:
            logger.error(f"运行过程中发生错误: {e}")
        finally:
            self.cleanup()
    
    def monitor_simple(self, duration_minutes):
        """简化的监控"""
        logger.info(f"开始监控，时长: {duration_minutes}分钟")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        question_count = 0
        video_count = 1
        
        while time.time() < end_time:
            try:
                # 检查题目（简化）
                if self.check_for_questions_simple():
                    logger.info(f"检测到题目，尝试处理...")
                    if self.answer_question_simple():
                        question_count += 1
                    time.sleep(5)
                
                # 检查视频是否结束
                if self.is_video_ended_simple():
                    logger.info(f"视频结束，尝试播放下一个...")
                    if self.go_to_next_video_simple():
                        video_count += 1
                        logger.info(f"开始第 {video_count} 个视频")
                        time.sleep(5)
                
                # 状态报告
                elapsed = int((time.time() - start_time) / 60)
                if elapsed > 0 and elapsed % 5 == 0:
                    logger.info(f"已运行 {elapsed} 分钟，处理了 {question_count} 个题目")
                
                time.sleep(10)  # 检查间隔
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"监控出错: {e}")
                time.sleep(10)
        
        logger.info(f"监控结束，处理了 {question_count} 个题目")
    
    def check_for_questions_simple(self):
        """简化的题目检查"""
        try:
            # 常见题目选择器
            selectors = [".question", ".quiz", ".exam", ".test", ".popup", ".dialog"]
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and elements[0].is_displayed():
                        return True
                except:
                    continue
            return False
        except:
            return False
    
    def answer_question_simple(self):
        """简化的答题"""
        try:
            # 随机选择答案
            answers = self.driver.find_elements(By.CSS_SELECTOR, ".option, .choice, input[type='radio'], input[type='checkbox']")
            if answers:
                random.choice(answers).click()
                time.sleep(1)
                
                # 尝试提交
                submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".submit, .confirm, button:contains('提交'), button:contains('确定')")
                if submit_buttons:
                    submit_buttons[0].click()
                    return True
            return False
        except:
            return False
    
    def is_video_ended_simple(self):
        """简化的视频结束检查"""
        try:
            # 检查视频元素
            js_script = """
            var videos = document.querySelectorAll('video');
            for (var i = 0; i < videos.length; i++) {
                if (videos[i].duration > 10 && videos[i].currentTime >= videos[i].duration - 5) {
                    return true;
                }
                if (videos[i].ended) {
                    return true;
                }
            }
            return false;
            """
            return self.driver.execute_script(js_script)
        except:
            return False
    
    def go_to_next_video_simple(self):
        """简化的下一个视频"""
        try:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, ".next, .next-btn, button:contains('下一'), button:contains('继续')")
            for btn in buttons:
                if btn.is_displayed() and btn.is_enabled():
                    btn.click()
                    return True
            return False
        except:
            return False
    
    def cleanup(self):
        """清理资源"""
        logger.info("正在关闭浏览器...")
        try:
            self.driver.quit()
            logger.info("浏览器已关闭")
        except:
            pass

def main_fixed():
    """修复版主函数"""
    print("=" * 60)
    print("修复版刷课自动化系统")
    print("解决空白页面问题")
    print("=" * 60)
    
    # 获取课程URL
    course_url = input("请输入课程页面URL: ").strip()
    if not course_url:
        print("❌ 必须提供课程URL")
        return
    
    # 简单配置
    print("\n使用默认配置:")
    print("  浏览器: Chrome")
    print("  平台: 智慧树")
    print("  模式: 手动模式（推荐）")
    
    # 登录信息
    use_login = input("\n是否需要自动登录？(y/n): ").strip().lower()
    username = None
    password = None
    
    if use_login == 'y':
        username = input("用户名: ").strip()
        password = input("密码: ").strip()
    
    # 时长
    try:
        duration = int(input("刷课时长（分钟）[默认60]: ").strip() or "60")
    except:
        duration = 60
    
    print("\n" + "=" * 60)
    print("开始运行...")
    print("=" * 60)
    
    # 创建并运行
    auto_course = CrossPlatformCourseAutomation(
        course_url=course_url,
        browser_type=BrowserType.CHROME,
        platform_type=PlatformType.ZHIHUISHU,
        username=username,
        password=password,
        headless=False  # 不使用无头模式，便于调试
    )
    
    auto_course.run_simple(duration, manual_mode=True)

if __name__ == "__main__":
    try:
        main_fixed()
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"程序出错: {e}")
        import traceback
        traceback.print_exc()