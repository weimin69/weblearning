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
            
            # 尝试自动登录
            time.sleep(3)
            logger.info("尝试自动登录...")
            
            # 根据不同平台使用不同的登录逻辑
            if self.platform_type == PlatformType.CHAOXING:
                # 学习通自动登录
                self._login_chaoxing()
            elif self.platform_type == PlatformType.ZHIHUISHU:
                # 智慧树自动登录
                self._login_zhihuishu()
            else:
                logger.info("该平台暂不支持自动登录")
                input("请手动登录，完成后按回车键继续...")
            
        except Exception as e:
            logger.error(f"登录过程中出错: {e}")
            logger.info("请手动登录")
            input("请手动登录，完成后按回车键继续...")
    
    def _login_chaoxing(self):
        """学习通自动登录"""
        try:
            logger.info("正在执行学习通自动登录...")
            
            # 查找用户名输入框
            username_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[name='uname'], input[name='username'], input[type='text'], input[placeholder*='账号'], input[placeholder*='用户名']")
            
            if username_inputs:
                username_input = username_inputs[0]
                username_input.clear()
                username_input.send_keys(self.username)
                logger.info("已输入用户名")
                time.sleep(1)
            else:
                logger.warning("未找到用户名输入框")
                raise Exception("未找到用户名输入框")
            
            # 查找密码输入框
            password_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[name='password'], input[type='password'], input[placeholder*='密码']")
            
            if password_inputs:
                password_input = password_inputs[0]
                password_input.clear()
                password_input.send_keys(self.password)
                logger.info("已输入密码")
                time.sleep(1)
            else:
                logger.warning("未找到密码输入框")
                raise Exception("未找到密码输入框")
            
            # 查找登录按钮
            login_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".login-btn, button[type='submit'], button:contains('登录'), input[type='submit']")
            
            if login_buttons:
                login_button = login_buttons[0]
                login_button.click()
                logger.info("已点击登录按钮")
            else:
                # 尝试通过JavaScript点击
                self.driver.execute_script("""
                    var buttons = document.querySelectorAll('.login-btn, button[type="submit"], button:contains("登录"), input[type="submit"]');
                    if (buttons.length > 0) {
                        buttons[0].click();
                        console.log('通过JS点击登录按钮');
                    }
                """)
                logger.info("通过JavaScript点击登录按钮")
            
            # 等待登录完成
            time.sleep(5)
            self.wait_for_page_load(10)
            
            # 检查是否登录成功
            current_url = self.driver.current_url
            if "i.chaoxing.com" in current_url or "passport2.chaoxing.com" not in current_url:
                logger.info("学习通登录成功！")
            else:
                logger.warning("登录可能未成功，请检查")
                
        except Exception as e:
            logger.error(f"学习通自动登录失败: {e}")
            raise
    
    def _login_zhihuishu(self):
        """智慧树自动登录"""
        try:
            logger.info("正在执行智慧树自动登录...")
            
            # 查找用户名输入框
            username_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[name='username'], input[type='text'], input[placeholder*='账号'], input[placeholder*='用户名']")
            
            if username_inputs:
                username_input = username_inputs[0]
                username_input.clear()
                username_input.send_keys(self.username)
                logger.info("已输入用户名")
                time.sleep(1)
            else:
                logger.warning("未找到用户名输入框")
                raise Exception("未找到用户名输入框")
            
            # 查找密码输入框
            password_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[name='password'], input[type='password'], input[placeholder*='密码']")
            
            if password_inputs:
                password_input = password_inputs[0]
                password_input.clear()
                password_input.send_keys(self.password)
                logger.info("已输入密码")
                time.sleep(1)
            else:
                logger.warning("未找到密码输入框")
                raise Exception("未找到密码输入框")
            
            # 查找登录按钮
            login_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".submit-btn, button[type='submit'], button:contains('登录'), input[type='submit']")
            
            if login_buttons:
                login_button = login_buttons[0]
                login_button.click()
                logger.info("已点击登录按钮")
            else:
                # 尝试通过JavaScript点击
                self.driver.execute_script("""
                    var buttons = document.querySelectorAll('.submit-btn, button[type="submit"], button:contains("登录"), input[type="submit"]');
                    if (buttons.length > 0) {
                        buttons[0].click();
                        console.log('通过JS点击登录按钮');
                    }
                """)
                logger.info("通过JavaScript点击登录按钮")
            
            # 等待登录完成
            time.sleep(5)
            self.wait_for_page_load(10)
            
            logger.info("智慧树登录完成")
                
        except Exception as e:
            logger.error(f"智慧树自动登录失败: {e}")
            raise
    
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
        last_activity_time = time.time()
        last_bypass_time = time.time()
        
        # 如果是学习通，初始化防挂机设置
        if self.platform_type == PlatformType.CHAOXING:
            self._init_anti_idle_protection()
        
        while time.time() < end_time:
            try:
                current_time = time.time()
                
                # 如果是学习通平台，定期执行防挂机绕过
                if self.platform_type == PlatformType.CHAOXING:
                    # 每25-35秒随机执行一次防挂机绕过（更自然）
                    if current_time - last_bypass_time > random.randint(25, 35):
                        self._bypass_chaoxing_anti_idle()
                        last_bypass_time = current_time
                    
                    # 每10秒执行一次轻量级活动模拟（更频繁但轻微）
                    if current_time - last_activity_time > 10:
                        self._simulate_light_activity()
                        last_activity_time = current_time
                
                # 检查题目（简化）
                if self.check_for_questions_simple():
                    logger.info(f"检测到题目，尝试处理...")
                    if self.answer_question_simple():
                        question_count += 1
                    
                    # 答题后尝试恢复视频播放
                    logger.info("答题完成，尝试恢复视频播放...")
                    self.resume_video_playback()
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
                    # 如果是学习通，额外报告防挂机状态
                    if self.platform_type == PlatformType.CHAOXING:
                        bypass_count = int((current_time - start_time) / 30)
                        logger.info(f"防挂机绕过已执行约 {bypass_count} 次")
                
                time.sleep(random.randint(8, 12))  # 随机检查间隔，更自然
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"监控出错: {e}")
                time.sleep(10)
        
        logger.info(f"监控结束，处理了 {question_count} 个题目")
        if self.platform_type == PlatformType.CHAOXING:
            total_time = (time.time() - start_time) / 60
            logger.info(f"学习通防挂机保护已启用 {total_time:.1f} 分钟")
    
    def resume_video_playback(self):
        """恢复视频播放"""
        try:
            logger.info("正在尝试恢复视频播放...")
            
            # 尝试点击播放按钮
            play_selectors = [
                ".play-btn", ".video-play", ".vjs-play-button",
                ".anticon-play", ".icon-play", "[class*='play']",
                "button[title*='播放']", "button[aria-label*='播放']"
            ]
            
            for selector in play_selectors:
                try:
                    play_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in play_buttons:
                        if btn.is_displayed():
                            btn.click()
                            logger.info(f"已点击播放按钮: {selector}")
                            time.sleep(1)
                            return True
                except:
                    continue
            
            # 尝试通过JavaScript控制视频播放
            js_script = """
            var videos = document.querySelectorAll('video');
            for (var i = 0; i < videos.length; i++) {
                if (videos[i].paused) {
                    videos[i].play();
                    console.log('通过JS恢复视频播放');
                    return true;
                }
            }
            return false;
            """
            
            result = self.driver.execute_script(js_script)
            if result:
                logger.info("通过JavaScript恢复视频播放")
                return True
            
            # 如果以上方法都失败，尝试按空格键播放
            self.action.send_keys(Keys.SPACE).perform()
            logger.info("已按空格键尝试播放视频")
            time.sleep(1)
            
            return True
            
        except Exception as e:
            logger.warning(f"恢复视频播放失败: {e}")
            return False
    
    def check_for_questions_simple(self):
        """简化的题目检查"""
        try:
            # 常见题目选择器
            selectors = [
                ".question", ".quiz", ".exam", ".test", ".popup", ".dialog",
                ".ant-modal", ".modal", ".pop-quiz", ".video-quiz",
                ".chaoxing-question", ".cx-question"  # 学习通特定选择器
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        try:
                            if element.is_displayed():
                                # 检查元素是否包含题目相关文本
                                element_text = element.text.lower()
                                if any(keyword in element_text for keyword in ['题目', '问题', 'quiz', 'question', '测试', 'exam']):
                                    logger.info(f"检测到题目弹窗: {selector}")
                                    return True
                        except:
                            continue
                except:
                    continue
            
            # 额外检查学习通特定的题目元素
            if self.platform_type == PlatformType.CHAOXING:
                return self._check_chaoxing_questions()
            
            return False
        except:
            return False
    
    def _check_chaoxing_questions(self):
        """检查学习通题目"""
        try:
            # 学习通题目常见选择器
            chaoxing_selectors = [
                ".ans-attach-ct",  # 学习通答题容器
                ".ans-job-icon",   # 学习通作业图标
                ".topic-item",     # 题目项
                ".tk-item",        # 题库项
                ".answer-box",     # 答题框
                ".question-box"    # 问题框
            ]
            
            for selector in chaoxing_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        try:
                            if element.is_displayed():
                                logger.info(f"检测到学习通题目: {selector}")
                                return True
                        except:
                            continue
                except:
                    continue
            
            return False
        except Exception as e:
            logger.warning(f"检查学习通题目失败: {e}")
            return False
    
    def answer_question_simple(self):
        """简化的答题"""
        try:
            # 如果是学习通平台，使用专门的答题方法
            if self.platform_type == PlatformType.CHAOXING:
                return self._answer_chaoxing_question()
            
            # 通用答题逻辑
            return self._answer_general_question()
            
        except Exception as e:
            logger.error(f"答题时出错: {e}")
            return False
    
    def _answer_general_question(self):
        """通用答题逻辑"""
        try:
            # 查找所有可能的答案选项
            answer_selectors = [
                ".option", ".choice", ".answer-option",
                "input[type='radio']", "input[type='checkbox']",
                ".radio", ".checkbox", ".ant-radio", ".ant-checkbox",
                ".option-item", ".choice-item"
            ]
            
            answers = []
            for selector in answer_selectors:
                try:
                    found = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if found:
                        answers.extend(found)
                except:
                    continue
            
            if not answers:
                logger.warning("未找到答案选项")
                return False
            
            # 随机选择答案
            if answers:
                selected_answer = random.choice(answers)
                try:
                    selected_answer.click()
                    logger.info("已选择答案")
                    time.sleep(1)
                except:
                    # 如果点击失败，尝试JavaScript点击
                    self.driver.execute_script("arguments[0].click();", selected_answer)
                    logger.info("通过JavaScript选择答案")
                    time.sleep(1)
                
                # 尝试提交
                submit_selectors = [
                    ".submit", ".confirm", ".submit-btn", ".confirm-btn",
                    "button:contains('提交')", "button:contains('确定')",
                    "button:contains('下一题')", "button:contains('继续')"
                ]
                
                for selector in submit_selectors:
                    try:
                        submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for btn in submit_buttons:
                            if btn.is_displayed() and btn.is_enabled():
                                btn.click()
                                logger.info("已提交答案")
                                time.sleep(2)
                                return True
                    except:
                        continue
                
                logger.warning("未找到提交按钮")
                return False
            
            return False
        except Exception as e:
            logger.error(f"通用答题失败: {e}")
            return False
    
    def _answer_chaoxing_question(self):
        """学习通答题逻辑"""
        try:
            logger.info("正在处理学习通题目...")
            
            # 查找学习通答案选项
            answer_selectors = [
                ".tkRadio", ".tkCheck",  # 学习通单选/多选
                ".answerOption", ".option-item",
                "input[name^='answer']", "input[type='radio']", "input[type='checkbox']",
                ".ant-radio-wrapper", ".ant-checkbox-wrapper"
            ]
            
            answers = []
            for selector in answer_selectors:
                try:
                    found = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if found:
                        answers.extend(found)
                except:
                    continue
            
            if not answers:
                logger.warning("未找到学习通答案选项")
                # 尝试通用答题方法
                return self._answer_general_question()
            
            # 随机选择答案
            selected_answer = random.choice(answers)
            try:
                selected_answer.click()
                logger.info("已选择学习通答案")
                time.sleep(1)
            except:
                self.driver.execute_script("arguments[0].click();", selected_answer)
                logger.info("通过JavaScript选择学习通答案")
                time.sleep(1)
            
            # 查找学习通提交按钮
            submit_selectors = [
                ".bluebtn", ".btn-blue",  # 学习通蓝色按钮
                ".ant-btn-primary", ".submitBtn",
                "button:contains('提交')", "button:contains('确定')",
                "button:contains('下一题')", "button:contains('继续')"
            ]
            
            submitted = False
            for selector in submit_selectors:
                try:
                    submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in submit_buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            logger.info("已提交学习通答案")
                            submitted = True
                            time.sleep(2)
                            break
                    if submitted:
                        break
                except:
                    continue
            
            if not submitted:
                logger.warning("未找到学习通提交按钮，尝试关闭弹窗")
                self.close_popup()
            
            return submitted
            
        except Exception as e:
            logger.error(f"学习通答题失败: {e}")
            return False
    
    def close_popup(self):
        """关闭弹窗"""
        try:
            # 查找关闭按钮
            close_selectors = [
                ".close", ".close-btn", ".modal-close",
                ".ant-modal-close", ".icon-close",
                "button[aria-label='Close']", "button:contains('关闭')",
                "button:contains('取消')", ".cancel-btn"
            ]
            
            for selector in close_selectors:
                try:
                    close_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in close_buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            logger.info("已关闭弹窗")
                            time.sleep(1)
                            return True
                except:
                    continue
            
            # 如果没有找到关闭按钮，尝试按ESC键
            self.action.send_keys(Keys.ESCAPE).perform()
            logger.info("已按ESC键关闭弹窗")
            time.sleep(1)
            return True
            
        except Exception as e:
            logger.warning(f"关闭弹窗失败: {e}")
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
            video_ended = self.driver.execute_script(js_script)
            
            # 如果是学习通平台，额外检查右侧视频选择栏的对勾
            if self.platform_type == PlatformType.CHAOXING:
                return self._check_chaoxing_video_completed() or video_ended
            
            return video_ended
        except:
            return False
    
    def _check_chaoxing_video_completed(self):
        """检查学习通视频是否完成（右侧视频选择栏对勾）"""
        try:
            # 查找学习通右侧视频列表中的对勾标记
            js_script = """
            // 查找学习通视频列表中的完成标记
            var completed_indicators = document.querySelectorAll('.icon-check, .icon-complete, .icon-done, .icon-finish, .anticon-check, [class*="check"], [class*="complete"], [class*="done"], [class*="finish"]');
            
            // 查找当前活动的视频项
            var active_items = document.querySelectorAll('.video-item.active, .lesson-item.active, .course-item.active, [class*="item"][class*="active"], .ant-list-item-active');
            
            // 检查当前活动项是否有完成标记
            for (var i = 0; i < active_items.length; i++) {
                var item = active_items[i];
                // 检查元素内部是否有对勾图标
                var check_icons = item.querySelectorAll('.icon-check, .icon-complete, .anticon-check, svg[aria-label*="check"], svg[aria-label*="完成"]');
                if (check_icons.length > 0) {
                    return true;
                }
                
                // 检查元素是否有表示完成的类名
                if (item.classList.contains('completed') || item.classList.contains('finished') || 
                    item.classList.contains('done') || item.classList.contains('passed')) {
                    return true;
                }
            }
            
            // 检查整个页面是否有明显的完成标记
            if (completed_indicators.length > 0) {
                // 检查这些标记是否可见
                for (var i = 0; i < completed_indicators.length; i++) {
                    if (completed_indicators[i].offsetParent !== null && 
                        completed_indicators[i].getBoundingClientRect().width > 0) {
                        return true;
                    }
                }
            }
            
            return false;
            """
            
            return self.driver.execute_script(js_script)
        except Exception as e:
            logger.warning(f"检查学习通视频完成状态失败: {e}")
            return False
    
    def go_to_next_video_simple(self):
        """简化的下一个视频"""
        try:
            # 如果是学习通平台，使用专门的方法
            if self.platform_type == PlatformType.CHAOXING:
                return self._go_to_next_chaoxing_video()
            
            # 通用方法
            return self._go_to_next_general_video()
        except Exception as e:
            logger.error(f"播放下一个视频失败: {e}")
            return False
    
    def _go_to_next_general_video(self):
        """通用播放下一个视频方法"""
        try:
            # 常见的下一个视频按钮选择器
            next_selectors = [
                ".next", ".next-btn", ".next-video", ".next-chapter",
                "button:contains('下一')", "button:contains('继续')",
                "button:contains('下一节')", "button:contains('下一章')",
                ".vjs-next-button", ".video-next", ".continue-btn"
            ]
            
            for selector in next_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            logger.info(f"点击下一个视频按钮: {selector}")
                            time.sleep(3)  # 等待页面加载
                            return True
                except:
                    continue
            
            logger.warning("未找到下一个视频按钮")
            return False
            
        except Exception as e:
            logger.error(f"通用播放下一个视频失败: {e}")
            return False
    
    def _go_to_next_chaoxing_video(self):
        """学习通播放下一个视频"""
        try:
            logger.info("正在查找学习通下一个视频...")
            
            # 学习通特定的下一个按钮选择器
            chaoxing_selectors = [
                ".next-btn", ".nextChapter", ".next_page",  # 学习通特定
                ".bluebtn", ".btn-blue",  # 学习通蓝色按钮
                ".ant-btn-primary:contains('下一节')",
                ".ant-btn:contains('继续学习')",
                "button:contains('下一节')", "button:contains('继续学习')",
                "button:contains('下一章')", "button:contains('下一个')"
            ]
            
            for selector in chaoxing_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            logger.info(f"点击学习通下一个视频按钮: {selector}")
                            time.sleep(3)
                            return True
                except:
                    continue
            
            # 如果没找到按钮，尝试通过课程目录选择下一个视频
            logger.info("尝试通过课程目录选择下一个视频...")
            if self._select_next_video_from_chaoxing_catalog():
                return True
            
            # 尝试JavaScript方法
            logger.info("尝试通过JavaScript查找下一个视频...")
            js_script = """
            // 查找学习通课程目录
            var catalogItems = document.querySelectorAll('.chapterItem, .sectionItem, .videoItem, .ant-list-item');
            var currentIndex = -1;
            
            // 查找当前活动的项目
            for (var i = 0; i < catalogItems.length; i++) {
                if (catalogItems[i].classList.contains('active') || 
                    catalogItems[i].classList.contains('current') ||
                    catalogItems[i].querySelector('.playing')) {
                    currentIndex = i;
                    break;
                }
            }
            
            // 如果找到当前项目，点击下一个
            if (currentIndex !== -1 && currentIndex + 1 < catalogItems.length) {
                catalogItems[currentIndex + 1].click();
                console.log('点击课程目录中的下一个项目');
                return true;
            }
            
            // 查找学习通的下一个按钮
            var nextButtons = document.querySelectorAll('.next-btn, .nextChapter, .bluebtn, .ant-btn-primary');
            for (var i = 0; i < nextButtons.length; i++) {
                var btn = nextButtons[i];
                var btnText = btn.textContent || btn.innerText;
                if (btnText.includes('下一') || btnText.includes('继续') || 
                    btnText.includes('next') || btnText.includes('Next')) {
                    if (btn.offsetParent !== null && !btn.disabled) {
                        btn.click();
                        console.log('通过JS点击学习通下一个按钮');
                        return true;
                    }
                }
            }
            
            return false;
            """
            
            result = self.driver.execute_script(js_script)
            if result:
                logger.info("通过JavaScript成功跳转到下一个视频")
                time.sleep(3)
                return True
            
            logger.warning("未找到学习通下一个视频")
            return False
            
        except Exception as e:
            logger.error(f"学习通播放下一个视频失败: {e}")
            return False
    
    def _select_next_video_from_chaoxing_catalog(self):
        """从学习通课程目录选择下一个视频"""
        try:
            # 查找课程目录项
            catalog_items = self.driver.find_elements(By.CSS_SELECTOR, 
                ".chapterItem, .sectionItem, .videoItem, .ant-list-item, .catalog-item, .course-item")
            
            if not catalog_items:
                return False
            
            current_index = -1
            
            # 查找当前活动的项目
            for i, item in enumerate(catalog_items):
                try:
                    classes = item.get_attribute("class") or ""
                    if "active" in classes or "current" in classes:
                        current_index = i
                        break
                    
                    # 检查是否有播放图标
                    playing_icons = item.find_elements(By.CSS_SELECTOR, 
                        ".icon-play, .anticon-play, .playing, .is-playing")
                    if playing_icons:
                        current_index = i
                        break
                except:
                    continue
            
            # 如果找到当前项目，点击下一个
            if current_index != -1 and current_index + 1 < len(catalog_items):
                try:
                    next_item = catalog_items[current_index + 1]
                    next_item.click()
                    logger.info("点击课程目录中的下一个项目")
                    time.sleep(3)
                    return True
                except:
                    # 如果点击失败，尝试JavaScript点击
                    self.driver.execute_script("arguments[0].click();", next_item)
                    logger.info("通过JavaScript点击课程目录中的下一个项目")
                    time.sleep(3)
                    return True
            
            return False
            
        except Exception as e:
            logger.warning(f"从课程目录选择下一个视频失败: {e}")
            return False
    
    def _bypass_chaoxing_anti_idle(self):
        """绕过学习通防挂机检测"""
        try:
            logger.info("执行防挂机绕过...")
            
            # 方法1: 模拟鼠标移动（轻微移动，不离开浏览器窗口）
            self._simulate_mouse_activity()
            
            # 方法2: 模拟键盘活动（轻微按键）
            self._simulate_keyboard_activity()
            
            # 方法3: 保持页面焦点和激活状态
            self._keep_page_active()
            
            # 方法4: 检查并恢复视频播放状态
            self._check_and_resume_video()
            
            logger.info("防挂机绕过完成")
            return True
            
        except Exception as e:
            logger.warning(f"防挂机绕过失败: {e}")
            return False
    
    def _simulate_mouse_activity(self):
        """模拟鼠标活动"""
        try:
            # 获取当前鼠标位置
            current_position = self.driver.get_window_position()
            
            # 轻微移动鼠标（在浏览器窗口内）
            new_x = current_position['x'] + random.randint(-5, 5)
            new_y = current_position['y'] + random.randint(-5, 5)
            
            # 移动鼠标到新位置
            self.driver.execute_script(f"""
                // 创建鼠标移动事件
                var event = new MouseEvent('mousemove', {{
                    view: window,
                    bubbles: true,
                    cancelable: true,
                    clientX: {new_x},
                    clientY: {new_y}
                }});
                document.dispatchEvent(event);
                
                // 触发一些鼠标相关事件
                var body = document.body;
                if (body) {{
                    body.dispatchEvent(new MouseEvent('mouseover', {{ bubbles: true }}));
                    body.dispatchEvent(new MouseEvent('mousemove', {{ bubbles: true }}));
                }}
                
                console.log('模拟鼠标移动');
            """)
            
            logger.debug("模拟鼠标移动完成")
            time.sleep(0.5)
            
        except Exception as e:
            logger.debug(f"模拟鼠标活动失败: {e}")
    
    def _simulate_keyboard_activity(self):
        """模拟键盘活动"""
        try:
            # 随机按一些无害的键（如Tab、方向键）
            keys = [Keys.TAB, Keys.ARROW_UP, Keys.ARROW_DOWN, Keys.ARROW_LEFT, Keys.ARROW_RIGHT]
            key_to_press = random.choice(keys)
            
            # 发送按键到body元素
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(key_to_press)
            
            logger.debug(f"模拟按键: {key_to_press}")
            time.sleep(0.5)
            
            # 也可以通过JavaScript触发键盘事件
            self.driver.execute_script("""
                // 触发键盘事件
                var event = new KeyboardEvent('keydown', {
                    key: 'Tab',
                    code: 'Tab',
                    keyCode: 9,
                    bubbles: true
                });
                document.dispatchEvent(event);
                
                // 触发焦点事件
                document.dispatchEvent(new FocusEvent('focus', { bubbles: true }));
                window.dispatchEvent(new FocusEvent('focus', { bubbles: true }));
                
                console.log('模拟键盘活动');
            """)
            
        except Exception as e:
            logger.debug(f"模拟键盘活动失败: {e}")
    
    def _keep_page_active(self):
        """保持页面激活状态"""
        try:
            # 方法1: 切换标签页焦点（通过JavaScript）
            self.driver.execute_script("""
                // 触发页面可见性相关事件
                if (document.hidden !== undefined) {
                    // 强制页面为可见状态
                    Object.defineProperty(document, 'hidden', { value: false });
                    Object.defineProperty(document, 'visibilityState', { value: 'visible' });
                    
                    // 触发visibilitychange事件
                    var event = new Event('visibilitychange');
                    document.dispatchEvent(event);
                }
                
                // 触发焦点事件
                window.dispatchEvent(new FocusEvent('focus'));
                document.dispatchEvent(new FocusEvent('focus'));
                
                // 触发页面活动事件
                window.dispatchEvent(new Event('pageshow'));
                window.dispatchEvent(new Event('load'));
                
                // 更新最后活动时间
                if (window.lastActivityTime) {
                    window.lastActivityTime = Date.now();
                }
                
                console.log('保持页面激活状态');
            """)
            
            # 方法2: 修改document.hasFocus()返回值
            self.driver.execute_script("""
                // 重写hasFocus方法，始终返回true
                var originalHasFocus = document.hasFocus;
                document.hasFocus = function() {
                    return true;
                };
                
                // 临时重写，5秒后恢复
                setTimeout(function() {
                    document.hasFocus = originalHasFocus;
                }, 5000);
            """)
            
            # 方法3: 触发resize事件（模拟窗口活动）
            self.driver.execute_script("""
                window.dispatchEvent(new Event('resize'));
                console.log('触发resize事件');
            """)
            
            logger.debug("保持页面激活状态完成")
            
        except Exception as e:
            logger.debug(f"保持页面激活状态失败: {e}")
    
    def _check_and_resume_video(self):
        """检查并恢复视频播放"""
        try:
            # 检查视频是否在播放
            js_script = """
            var videos = document.querySelectorAll('video');
            for (var i = 0; i < videos.length; i++) {
                if (videos[i].paused && !videos[i].ended) {
                    // 视频暂停但未结束，尝试播放
                    videos[i].play().catch(function(e) {
                        console.log('自动播放失败:', e);
                    });
                    return true;
                }
            }
            return false;
            """
            
            video_was_paused = self.driver.execute_script(js_script)
            if video_was_paused:
                logger.info("检测到视频暂停，已尝试恢复播放")
            
            # 检查页面是否有挂机检测弹窗
            self._check_for_idle_popup()
            
            return True
            
        except Exception as e:
            logger.debug(f"检查并恢复视频失败: {e}")
            return False
    
    def _check_for_idle_popup(self):
        """检查并关闭挂机检测弹窗"""
        try:
            # 学习通常见的挂机检测弹窗选择器
            idle_popup_selectors = [
                ".idle-popup", ".anti-idle", ".inactive-alert",
                ".modal:contains('检测到您可能离开')",
                ".modal:contains('长时间无操作')",
                ".dialog:contains('挂机')",
                ".alert:contains('活动')",
                ".chaoxing-idle-check",  # 学习通特定
                ".cx-popup-idle"         # 学习通特定
            ]
            
            for selector in idle_popup_selectors:
                try:
                    popups = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for popup in popups:
                        if popup.is_displayed():
                            logger.warning("检测到挂机检测弹窗，尝试关闭...")
                            
                            # 查找关闭或确认按钮
                            close_buttons = popup.find_elements(By.CSS_SELECTOR, 
                                ".close, .confirm, .ok-btn, button:contains('确定'), button:contains('继续'), button:contains('我知道了')")
                            
                            if close_buttons:
                                close_buttons[0].click()
                                logger.info("已关闭挂机检测弹窗")
                                time.sleep(1)
                                return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            logger.debug(f"检查挂机检测弹窗失败: {e}")
            return False
    
    def _init_anti_idle_protection(self):
        """初始化防挂机保护"""
        try:
            logger.info("初始化学习通防挂机保护...")
            
            # 第一步：注入基础防挂机保护
            js_init = """
            // 创建全局变量来跟踪活动状态
            window._chaoxingAntiIdle = {
                lastActivity: Date.now(),
                activityCount: 0,
                isProtected: true,
                mousePosition: { x: 0, y: 0 },
                mouseLocked: false,
                mouseInBrowser: true  // 始终标记鼠标在浏览器内
            };
            
            // 重写一些可能被检测的方法
            var originalHasFocus = document.hasFocus;
            document.hasFocus = function() {
                window._chaoxingAntiIdle.lastActivity = Date.now();
                return true; // 始终返回true，表示页面有焦点
            };
            
            // 监听visibilitychange事件
            document.addEventListener('visibilitychange', function() {
                window._chaoxingAntiIdle.lastActivity = Date.now();
                // 强制保持可见状态
                if (document.hidden) {
                    console.log('检测到页面隐藏，尝试保持激活...');
                }
            });
            
            console.log('基础防挂机保护已初始化');
            """
            
            self.driver.execute_script(js_init)
            logger.info("基础防挂机保护初始化完成")
            
            # 第二步：启用强制鼠标保持在浏览器内
            self._force_mouse_in_browser()
            
            # 第三步：设置鼠标陷阱
            self._setup_mouse_trap()
            
            # 第四步：注入增强的鼠标控制
            self._inject_enhanced_mouse_control()
            
            logger.info("所有防挂机保护组件已初始化完成")
            
        except Exception as e:
            logger.warning(f"初始化防挂机保护失败: {e}")
    
    def _inject_enhanced_mouse_control(self):
        """注入增强的鼠标控制脚本"""
        try:
            js_enhanced = """
            // 增强鼠标控制 - 专门针对学习通鼠标移出检测
            (function() {
                var mouseController = {
                    // 鼠标位置模拟
                    simulateMousePresence: function() {
                        // 在浏览器窗口内创建持续的鼠标活动
                        setInterval(function() {
                            // 随机位置（在窗口内）
                            var x = 100 + Math.random() * (window.innerWidth - 200);
                            var y = 100 + Math.random() * (window.innerHeight - 200);
                            
                            // 创建完整的鼠标事件序列
                            var events = [
                                { type: 'mousemove', x: x, y: y },
                                { type: 'mouseover', x: x, y: y },
                                { type: 'mousenter', x: x, y: y }
                            ];
                            
                            events.forEach(function(eventConfig) {
                                try {
                                    var event = new MouseEvent(eventConfig.type, {
                                        view: window,
                                        bubbles: true,
                                        cancelable: true,
                                        clientX: eventConfig.x,
                                        clientY: eventConfig.y
                                    });
                                    document.dispatchEvent(event);
                                } catch(e) {}
                            });
                            
                            // 更新全局状态
                            if (window._chaoxingAntiIdle) {
                                window._chaoxingAntiIdle.mousePosition.x = x;
                                window._chaoxingAntiIdle.mousePosition.y = y;
                                window._chaoxingAntiIdle.lastActivity = Date.now();
                                window._chaoxingAntiIdle.mouseInBrowser = true;
                            }
                            
                        }, 5000); // 每5秒模拟一次
                    },
                    
                    // 拦截和重写鼠标检测
                    interceptMouseDetection: function() {
                        // 拦截getBoundingClientRect等可能用于检测鼠标位置的方法
                        var elements = document.querySelectorAll('video, .video-player, .vjs-tech');
                        elements.forEach(function(element) {
                            var originalRect = element.getBoundingClientRect;
                            element.getBoundingClientRect = function() {
                                var rect = originalRect.call(this);
                                // 确保rect总是有效的（鼠标在区域内）
                                if (rect.width > 0 && rect.height > 0) {
                                    // 模拟鼠标在视频元素上
                                    if (window._chaoxingAntiIdle) {
                                        window._chaoxingAntiIdle.mousePosition.x = rect.left + rect.width / 2;
                                        window._chaoxingAntiIdle.mousePosition.y = rect.top + rect.height / 2;
                                    }
                                }
                                return rect;
                            };
                        });
                    },
                    
                    // 创建虚拟鼠标层
                    createVirtualMouseLayer: function() {
                        var layer = document.createElement('div');
                        layer.id = '_chaoxing_mouse_layer';
                        layer.style.cssText = `
                            position: fixed;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            pointer-events: none;
                            z-index: 2147483647;
                            background: transparent;
                        `;
                        
                        // 在层上持续触发鼠标事件
                        setInterval(function() {
                            var event = new MouseEvent('mousemove', {
                                view: window,
                                bubbles: false,
                                cancelable: false,
                                clientX: window.innerWidth / 2,
                                clientY: window.innerHeight / 2
                            });
                            layer.dispatchEvent(event);
                        }, 3000);
                        
                        document.body.appendChild(layer);
                    },
                    
                    // 启动所有控制
                    start: function() {
                        this.simulateMousePresence();
                        this.interceptMouseDetection();
                        this.createVirtualMouseLayer();
                        console.log('增强鼠标控制已启动');
                    }
                };
                
                // 延迟启动，确保页面加载完成
                setTimeout(function() {
                    mouseController.start();
                }, 2000);
                
                // 暴露控制器
                window._chaoxingMouseController = mouseController;
                
            })();
            """
            
            self.driver.execute_script(js_enhanced)
            logger.info("增强鼠标控制已注入")
            
        except Exception as e:
            logger.warning(f"注入增强鼠标控制失败: {e}")
    
    def _simulate_light_activity(self):
        """模拟轻量级用户活动"""
        try:
            # 随机选择一种轻量级活动
            activities = [
                self._simulate_mouse_hover,
                self._simulate_scroll_slight,
                self._simulate_document_activity,
                self._simulate_window_focus
            ]
            
            activity = random.choice(activities)
            activity()
            logger.debug("执行轻量级活动模拟")
            
        except Exception as e:
            logger.debug(f"轻量级活动模拟失败: {e}")
    
    def _simulate_mouse_hover(self):
        """模拟鼠标悬停"""
        try:
            self.driver.execute_script("""
                // 在随机位置触发mouseover事件
                var x = Math.random() * window.innerWidth;
                var y = Math.random() * window.innerHeight;
                
                var event = new MouseEvent('mouseover', {
                    view: window,
                    bubbles: true,
                    cancelable: true,
                    clientX: x,
                    clientY: y
                });
                
                document.elementFromPoint(x, y).dispatchEvent(event);
                console.log('模拟鼠标悬停');
            """)
        except:
            pass
    
    def _simulate_scroll_slight(self):
        """模拟轻微滚动"""
        try:
            # 轻微滚动几个像素
            scroll_amount = random.randint(-3, 3)
            self.driver.execute_script(f"""
                window.scrollBy(0, {scroll_amount});
                // 触发scroll事件
                var event = new Event('scroll', {{ bubbles: true }});
                window.dispatchEvent(event);
                console.log('模拟轻微滚动');
            """)
        except:
            pass
    
    def _simulate_document_activity(self):
        """模拟文档活动"""
        try:
            self.driver.execute_script("""
                // 触发各种文档事件
                var events = ['mousemove', 'mouseenter', 'mouseleave', 'click'];
                events.forEach(function(eventType) {
                    var event = new Event(eventType, { bubbles: true });
                    document.dispatchEvent(event);
                });
                
                // 更新文档活动时间
                if (document.lastModified) {
                    // 轻微修改文档属性来模拟活动
                    Object.defineProperty(document, 'lastModified', {
                        value: new Date().toISOString()
                    });
                }
                
                console.log('模拟文档活动');
            """)
        except:
            pass
    
    def _simulate_window_focus(self):
        """模拟窗口焦点"""
        try:
            self.driver.execute_script("""
                // 触发窗口焦点事件
                window.dispatchEvent(new FocusEvent('focus'));
                window.dispatchEvent(new FocusEvent('blur'));
                window.dispatchEvent(new FocusEvent('focus')); // 再次获得焦点
                
                // 触发页面可见性事件
                if (document.visibilityState) {
                    var event = new Event('visibilitychange');
                    document.dispatchEvent(event);
                }
                
                console.log('模拟窗口焦点变化');
            """)
        except:
            pass
    
    def _force_mouse_in_browser(self):
        """强制鼠标保持在浏览器窗口内（操作系统级别）"""
        try:
            logger.info("启用强制鼠标保持在浏览器内功能...")
            
            # 获取浏览器窗口位置和大小
            window_rect = self.driver.get_window_rect()
            window_x = window_rect['x']
            window_y = window_rect['y']
            window_width = window_rect['width']
            window_height = window_rect['height']
            
            logger.info(f"浏览器窗口位置: ({window_x}, {window_y}), 大小: {window_width}x{window_height}")
            
            # 计算浏览器窗口中心点
            center_x = window_x + window_width // 2
            center_y = window_y + window_height // 2
            
            # 注入更强大的JavaScript鼠标控制
            js_mouse_control = """
            // 增强版鼠标控制
            window._chaoxingMouseControl = {
                isActive: true,
                lastMouseEvent: Date.now(),
                mouseInBrowser: true,
                
                // 强制鼠标在浏览器内
                forceMouseInBrowser: function() {
                    // 创建持续的鼠标存在事件
                    setInterval(function() {
                        // 触发鼠标移动事件（在浏览器中心区域）
                        var centerX = window.innerWidth / 2;
                        var centerY = window.innerHeight / 2;
                        
                        // 轻微随机偏移
                        var offsetX = (Math.random() - 0.5) * 50;
                        var offsetY = (Math.random() - 0.5) * 50;
                        
                        var mouseMoveEvent = new MouseEvent('mousemove', {
                            view: window,
                            bubbles: true,
                            cancelable: true,
                            clientX: centerX + offsetX,
                            clientY: centerY + offsetY,
                            movementX: offsetX,
                            movementY: offsetY
                        });
                        
                        document.dispatchEvent(mouseMoveEvent);
                        
                        // 同时触发其他鼠标事件
                        var events = ['mouseover', 'mousemove', 'mouseenter'];
                        events.forEach(function(eventType) {
                            var event = new MouseEvent(eventType, { 
                                bubbles: true,
                                clientX: centerX + offsetX,
                                clientY: centerY + offsetY
                            });
                            document.dispatchEvent(event);
                        });
                        
                        window._chaoxingMouseControl.lastMouseEvent = Date.now();
                        window._chaoxingMouseControl.mouseInBrowser = true;
                        
                    }, 3000); // 每3秒触发一次
                },
                
                // 拦截鼠标离开事件
                interceptMouseLeave: function() {
                    document.addEventListener('mouseleave', function(e) {
                        console.log('鼠标离开拦截: 模拟鼠标返回');
                        
                        // 立即创建鼠标进入事件
                        var mouseEnterEvent = new MouseEvent('mouseenter', {
                            bubbles: true,
                            clientX: window.innerWidth / 2,
                            clientY: window.innerHeight / 2
                        });
                        
                        // 先触发离开，然后立即触发进入
                        setTimeout(function() {
                            document.dispatchEvent(mouseEnterEvent);
                            
                            // 再触发移动事件
                            var mouseMoveEvent = new MouseEvent('mousemove', {
                                bubbles: true,
                                clientX: window.innerWidth / 2,
                                clientY: window.innerHeight / 2
                            });
                            document.dispatchEvent(mouseMoveEvent);
                        }, 10);
                        
                        e.stopImmediatePropagation();
                        return false;
                    }, true);
                },
                
                // 重写鼠标相关属性
                overrideMouseProperties: function() {
                    // 尝试重写document.elementFromPoint
                    var originalElementFromPoint = document.elementFromPoint;
                    document.elementFromPoint = function(x, y) {
                        window._chaoxingMouseControl.lastMouseEvent = Date.now();
                        var result = originalElementFromPoint.call(this, x, y);
                        if (!result) {
                            // 如果返回null（鼠标在窗口外），返回body元素
                            return document.body;
                        }
                        return result;
                    };
                    
                    // 记录鼠标坐标
                    Object.defineProperty(document, 'mouseX', {
                        get: function() { return window.innerWidth / 2; },
                        configurable: true
                    });
                    
                    Object.defineProperty(document, 'mouseY', {
                        get: function() { return window.innerHeight / 2; },
                        configurable: true
                    });
                }
            };
            
            // 启动所有控制
            window._chaoxingMouseControl.forceMouseInBrowser();
            window._chaoxingMouseControl.interceptMouseLeave();
            window._chaoxingMouseControl.overrideMouseProperties();
            
            console.log('增强版鼠标控制已启用');
            """
            
            self.driver.execute_script(js_mouse_control)
            logger.info("强制鼠标保持在浏览器内功能已启用")
            
            # 额外：通过ActionChains模拟鼠标活动
            self._simulate_mouse_with_actions(center_x, center_y, window_width, window_height)
            
            return True
            
        except Exception as e:
            logger.error(f"强制鼠标保持在浏览器内失败: {e}")
            return False
    
    def _simulate_mouse_with_actions(self, center_x, center_y, width, height):
        """使用ActionChains模拟鼠标活动"""
        try:
            # 将鼠标移动到浏览器窗口内
            action = ActionChains(self.driver)
            
            # 移动到浏览器中心（相对坐标）
            action.move_by_offset(width // 2, height // 2).perform()
            time.sleep(0.5)
            
            # 轻微移动鼠标
            for i in range(3):
                offset_x = random.randint(-20, 20)
                offset_y = random.randint(-20, 20)
                action.move_by_offset(offset_x, offset_y).perform()
                time.sleep(0.3)
            
            logger.debug("使用ActionChains模拟鼠标活动完成")
            
        except Exception as e:
            logger.debug(f"ActionChains模拟鼠标活动失败: {e}")
    
    def _setup_mouse_trap(self):
        """设置鼠标陷阱，防止鼠标移出"""
        try:
            logger.info("设置鼠标移出检测陷阱...")
            
            # 注入鼠标陷阱JavaScript
            js_mouse_trap = """
            // 鼠标陷阱 - 防止检测到鼠标离开
            (function() {
                var mouseTrap = {
                    initialized: false,
                    mousePresent: true,
                    
                    init: function() {
                        if (this.initialized) return;
                        
                        // 创建虚拟鼠标光标
                        this.createVirtualCursor();
                        
                        // 拦截所有鼠标离开相关事件
                        this.interceptEvents();
                        
                        // 定期报告鼠标存在
                        this.reportMousePresence();
                        
                        this.initialized = true;
                        console.log('鼠标陷阱已初始化');
                    },
                    
                    createVirtualCursor: function() {
                        // 创建隐藏的虚拟鼠标光标元素
                        var virtualCursor = document.createElement('div');
                        virtualCursor.id = '_chaoxing_virtual_cursor';
                        virtualCursor.style.cssText = `
                            position: fixed;
                            width: 1px;
                            height: 1px;
                            background: transparent;
                            pointer-events: none;
                            z-index: 999999;
                            top: 50%;
                            left: 50%;
                        `;
                        document.body.appendChild(virtualCursor);
                        
                        // 定期移动虚拟光标
                        setInterval(function() {
                            var cursor = document.getElementById('_chaoxing_virtual_cursor');
                            if (cursor) {
                                // 轻微随机移动
                                var offsetX = (Math.random() - 0.5) * 30;
                                var offsetY = (Math.random() - 0.5) * 30;
                                
                                cursor.style.left = (50 + offsetX) + '%';
                                cursor.style.top = (50 + offsetY) + '%';
                                
                                // 触发相关事件
                                var event = new MouseEvent('mousemove', {
                                    bubbles: true,
                                    clientX: window.innerWidth * (0.5 + offsetX/100),
                                    clientY: window.innerHeight * (0.5 + offsetY/100)
                                });
                                document.dispatchEvent(event);
                            }
                        }, 2000);
                    },
                    
                    interceptEvents: function() {
                        var eventsToIntercept = [
                            'mouseleave', 'mouseout', 'pointerleave'
                        ];
                        
                        eventsToIntercept.forEach(function(eventType) {
                            document.addEventListener(eventType, function(e) {
                                console.log('拦截到鼠标离开事件:', eventType);
                                
                                // 阻止事件传播
                                e.stopImmediatePropagation();
                                e.preventDefault();
                                
                                // 立即触发相反事件
                                var enterEvent = new MouseEvent(
                                    eventType.replace('leave', 'enter').replace('out', 'over'),
                                    { bubbles: true }
                                );
                                setTimeout(function() {
                                    document.dispatchEvent(enterEvent);
                                }, 1);
                                
                                return false;
                            }, true); // 捕获阶段
                        });
                    },
                    
                    reportMousePresence: function() {
                        setInterval(function() {
                            // 定期报告鼠标在页面内
                            var event = new CustomEvent('mousepresence', {
                                detail: { present: true, timestamp: Date.now() }
                            });
                            document.dispatchEvent(event);
                            
                            // 更新全局状态
                            if (window._chaoxingAntiIdle) {
                                window._chaoxingAntiIdle.lastActivity = Date.now();
                                window._chaoxingAntiIdle.mouseInBrowser = true;
                            }
                        }, 5000);
                    }
                };
                
                // 启动鼠标陷阱
                mouseTrap.init();
                
                // 暴露到全局
                window._chaoxingMouseTrap = mouseTrap;
                
            })();
            """
            
            self.driver.execute_script(js_mouse_trap)
            logger.info("鼠标陷阱已设置完成")
            
        except Exception as e:
            logger.warning(f"设置鼠标陷阱失败: {e}")
    
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