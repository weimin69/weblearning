#!/usr/bin/env python3
"""
跨平台刷课自动化系统
支持所有主流浏览器：Chrome, Firefox, Edge, Safari
功能：
1. 自动播放视频课程
2. 检测题目弹窗并随机选择答案
3. 自动关闭题目窗口
4. 自动查找并播放下一个视频
5. 全自动化连续播放
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
        self.driver = self._init_browser_driver()
        self.wait = WebDriverWait(self.driver, 15)
        self.action = ActionChains(self.driver)
        
        logger.info(f"{browser_type.value.capitalize()}浏览器已启动")
        logger.info(f"目标平台: {self.platform_configs[platform_type]['name']}")
    
    def _init_browser_driver(self):
        """根据浏览器类型初始化驱动，使用webdriver-manager自动管理驱动"""
        system = platform.system().lower()
        
        try:
            if self.browser_type == BrowserType.CHROME:
                from selenium.webdriver.chrome.service import Service as ChromeService
                from selenium.webdriver.chrome.options import Options as ChromeOptions
                from webdriver_manager.chrome import ChromeDriverManager
                
                chrome_options = ChromeOptions()
                chrome_options.add_argument("--start-maximized")
                chrome_options.add_argument("--disable-notifications")
                chrome_options.add_argument("--disable-popup-blocking")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                # 添加用户代理，模拟真实浏览器
                chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                
                # 更多反检测措施
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-web-security")
                chrome_options.add_argument("--allow-running-insecure-content")
                
                if self.headless:
                    chrome_options.add_argument("--headless")
                    chrome_options.add_argument("--no-sandbox")
                    chrome_options.add_argument("--disable-dev-shm-usage")
                
                # 使用webdriver-manager自动管理驱动
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=chrome_options)
            
            elif self.browser_type == BrowserType.FIREFOX:
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                from webdriver_manager.firefox import GeckoDriverManager
                
                firefox_options = FirefoxOptions()
                firefox_options.add_argument("--start-maximized")
                firefox_options.set_preference("dom.webnotifications.enabled", False)
                
                # 添加用户代理
                firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                
                # 更多反检测设置
                firefox_options.set_preference("dom.webdriver.enabled", False)
                firefox_options.set_preference("useAutomationExtension", False)
                
                if self.headless:
                    firefox_options.add_argument("--headless")
                
                # 使用webdriver-manager自动管理驱动
                service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=firefox_options)
            
            elif self.browser_type == BrowserType.EDGE:
                from selenium.webdriver.edge.service import Service as EdgeService
                from selenium.webdriver.edge.options import Options as EdgeOptions
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                
                edge_options = EdgeOptions()
                edge_options.add_argument("--start-maximized")
                edge_options.add_argument("--disable-notifications")
                edge_options.add_argument("--disable-popup-blocking")
                edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                edge_options.add_experimental_option('useAutomationExtension', False)
                
                # 添加用户代理
                edge_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                
                # 更多反检测措施
                edge_options.add_argument("--disable-gpu")
                edge_options.add_argument("--no-sandbox")
                edge_options.add_argument("--disable-dev-shm-usage")
                
                if self.headless:
                    edge_options.add_argument("--headless")
                    edge_options.add_argument("--no-sandbox")
                
                # 使用webdriver-manager自动管理驱动
                service = EdgeService(EdgeChromiumDriverManager().install())
                return webdriver.Edge(service=service, options=edge_options)
            
            elif self.browser_type == BrowserType.SAFARI:
                if system != "darwin":
                    raise Exception("Safari浏览器仅支持macOS系统")
                
                safari_options = webdriver.SafariOptions()
                return webdriver.Safari(options=safari_options)
            
            else:
                raise ValueError(f"不支持的浏览器类型: {self.browser_type}")
                
        except ImportError as e:
            logger.error(f"缺少必要的库: {e}")
            raise
        except Exception as e:
            logger.error(f"初始化浏览器驱动失败: {e}")
            # 如果webdriver-manager失败，尝试使用系统默认路径
            logger.info("尝试使用系统默认驱动路径...")
            return self._init_browser_driver_fallback()
    
    def _init_browser_driver_fallback(self):
        """备用的驱动初始化方法，使用系统默认路径"""
        system = platform.system().lower()
        
        try:
            if self.browser_type == BrowserType.CHROME:
                from selenium.webdriver.chrome.service import Service as ChromeService
                from selenium.webdriver.chrome.options import Options as ChromeOptions
                
                chrome_options = ChromeOptions()
                chrome_options.add_argument("--start-maximized")
                
                # 尝试常见路径
                paths = []
                if system == "darwin":
                    paths = ['/usr/local/bin/chromedriver', '/opt/homebrew/bin/chromedriver']
                elif system == "linux":
                    paths = ['/usr/bin/chromedriver', '/usr/local/bin/chromedriver']
                elif system == "windows":
                    paths = ['chromedriver.exe']
                
                for path in paths:
                    try:
                        service = ChromeService(path)
                        return webdriver.Chrome(service=service, options=chrome_options)
                    except:
                        continue
                
                # 如果所有路径都失败，尝试无service参数
                return webdriver.Chrome(options=chrome_options)
            
            elif self.browser_type == BrowserType.FIREFOX:
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                
                firefox_options = FirefoxOptions()
                firefox_options.add_argument("--start-maximized")
                
                # 尝试常见路径
                paths = []
                if system == "darwin":
                    paths = ['/usr/local/bin/geckodriver', '/opt/homebrew/bin/geckodriver']
                elif system == "linux":
                    paths = ['/usr/bin/geckodriver', '/usr/local/bin/geckodriver']
                elif system == "windows":
                    paths = ['geckodriver.exe']
                
                for path in paths:
                    try:
                        service = FirefoxService(path)
                        return webdriver.Firefox(service=service, options=firefox_options)
                    except:
                        continue
                
                # 如果所有路径都失败，尝试无service参数
                return webdriver.Firefox(options=firefox_options)
            
            else:
                # 对于其他浏览器，建议用户安装Chrome
                logger.error(f"无法初始化 {self.browser_type.value} 浏览器驱动")
                logger.info("建议安装Chrome浏览器或使用Chrome选项")
                raise
            
        except Exception as e:
            logger.error(f"备用驱动初始化也失败: {e}")
            raise
    
    def login(self):
        """登录平台（如果需要）"""
        if not self.username or not self.password:
            logger.info("未提供登录凭据，请手动登录")
            platform_name = self.platform_configs[self.platform_type]["name"]
            print(f"请手动登录 {platform_name} 平台")
            input("登录完成后按回车键继续...")
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
            # 访问登录页面（带页面检查）
            logger.info(f"访问登录页面: {login_url}")
            self.driver.get(login_url)
            
            # 等待页面加载
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                logger.info("登录页面加载完成")
                
                # 检查页面状态
                current_url = self.driver.current_url
                page_title = self.driver.title
                logger.info(f"当前URL: {current_url}")
                logger.info(f"页面标题: {page_title}")
                
                # 检查是否重定向到其他页面
                if "login" not in current_url.lower() and "signin" not in current_url.lower():
                    logger.info(f"已重定向到: {current_url}")
                    # 检查是否已登录
                    if any(keyword in page_title.lower() for keyword in ["首页", "主页", "dashboard", "个人中心"]):
                        logger.info("可能已自动登录或已在登录状态")
                        return
                
            except TimeoutException:
                logger.warning("登录页面加载超时，继续尝试")
            
            # 尝试多种登录方式
            login_selectors = [
                ".login-btn",
                ".login-link",
                "a[href*='login']",
                "button:contains('登录')",
                "a:contains('登录')",
                ".user-login",
                ".header-login"
            ]
            
            login_clicked = False
            for selector in login_selectors:
                try:
                    login_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in login_elements:
                        if element.is_displayed() and element.is_enabled():
                            element.click()
                            logger.info(f"点击登录按钮: {selector}")
                            login_clicked = True
                            time.sleep(2)
                            break
                    if login_clicked:
                        break
                except:
                    continue
            
            if not login_clicked:
                logger.warning("未找到登录按钮，尝试直接输入用户名密码")
            
            # 输入用户名和密码
            username_selectors = [
                "input[name='username']",
                "input[name='account']",
                "input[type='text']",
                "input[placeholder*='用户名']",
                "input[placeholder*='账号']",
                "#username",
                "#account"
            ]
            
            password_selectors = [
                "input[name='password']",
                "input[type='password']",
                "input[placeholder*='密码']",
                "#password"
            ]
            
            # 输入用户名
            username_found = False
            for selector in username_selectors:
                try:
                    username_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    username_input.clear()
                    username_input.send_keys(self.username)
                    logger.info("已输入用户名")
                    username_found = True
                    break
                except:
                    continue
            
            # 输入密码
            password_found = False
            for selector in password_selectors:
                try:
                    password_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    password_input.clear()
                    password_input.send_keys(self.password)
                    logger.info("已输入密码")
                    password_found = True
                    break
                except:
                    continue
            
            if not username_found or not password_found:
                logger.warning("未找到用户名或密码输入框，请手动登录")
                input("请手动登录，完成后按回车键继续...")
                return
            
            # 查找并点击提交按钮
            submit_selectors = [
                "button[type='submit']",
                ".submit-btn",
                "button:contains('登录')",
                "button:contains('登入')",
                "input[type='submit']"
            ]
            
            submitted = False
            for selector in submit_selectors:
                try:
                    submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in submit_buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            logger.info("已提交登录信息")
                            submitted = True
                            time.sleep(3)
                            break
                    if submitted:
                        break
                except:
                    continue
            
            if not submitted:
                # 尝试按回车键
                password_input.send_keys(Keys.RETURN)
                logger.info("已按回车键提交登录")
                time.sleep(3)
            
            # 检查登录是否成功
            time.sleep(5)
            if "login" not in self.driver.current_url.lower():
                logger.info("登录成功")
            else:
                logger.warning("登录可能失败，请检查用户名密码")
                input("请手动登录，完成后按回车键继续...")
                
        except Exception as e:
            logger.error(f"登录失败: {e}")
            logger.info("请手动登录")
            input("请手动登录，完成后按回车键继续...")
    
    def navigate_to_course(self, max_retries=3):
        """导航到课程页面（带重试机制）"""
        logger.info(f"正在访问课程页面: {self.course_url}")
        
        for attempt in range(max_retries):
            try:
                logger.info(f"尝试加载页面 (第{attempt + 1}次)...")
                self.driver.get(self.course_url)
                
                # 等待页面加载完成（更长的超时时间）
                wait_time = 10  # 秒
                logger.info(f"等待页面加载，超时时间: {wait_time}秒")
                
                # 等待页面完全加载
                WebDriverWait(self.driver, wait_time).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                
                # 检查页面是否有效
                current_url = self.driver.current_url
                page_title = self.driver.title
                page_source_length = len(self.driver.page_source)
                
                logger.info(f"页面加载成功:")
                logger.info(f"  URL: {current_url}")
                logger.info(f"  标题: {page_title}")
                logger.info(f"  页面大小: {page_source_length} 字符")
                
                # 检查页面内容是否有效
                if page_source_length < 1000:
                    logger.warning(f"页面内容过少 ({page_source_length} 字符)，可能加载失败")
                    if attempt < max_retries - 1:
                        logger.info(f"等待3秒后重试...")
                        time.sleep(3)
                        continue
                
                # 检查是否有错误页面
                page_text = self.driver.page_source.lower()
                error_keywords = ["error", "无法访问", "404", "not found", "timeout", "加载失败"]
                for keyword in error_keywords:
                    if keyword in page_text:
                        logger.warning(f"检测到错误关键词: {keyword}")
                        if attempt < max_retries - 1:
                            logger.info(f"等待3秒后重试...")
                            time.sleep(3)
                            continue
                
                logger.info("课程页面加载完成")
                return True
                
            except TimeoutException:
                logger.warning(f"页面加载超时 (第{attempt + 1}次)")
                if attempt < max_retries - 1:
                    logger.info("等待5秒后重试...")
                    time.sleep(5)
                else:
                    logger.error("页面加载多次超时，继续执行")
                    return False
                    
            except Exception as e:
                logger.error(f"页面加载出错 (第{attempt + 1}次): {e}")
                if attempt < max_retries - 1:
                    logger.info("等待5秒后重试...")
                    time.sleep(5)
                else:
                    logger.error("页面加载多次失败，继续执行")
                    return False
        
        return False
    
    def play_video(self):
        """开始播放视频"""
        logger.info("正在查找并播放视频...")
        
        try:
            # 常见的视频播放按钮选择器
            play_selectors = [
                ".play-btn",
                ".video-play",
                ".vjs-big-play-button",
                ".videojs-big-play-button",
                "[class*='play']",
                "button[title*='播放']",
                "button[aria-label*='播放']",
                ".video-js .vjs-big-play-button",
                ".video-player .play-button",
                ".course-video .play-btn",
                ".study-play",
                ".start-study"
            ]
            
            play_clicked = False
            
            for selector in play_selectors:
                try:
                    play_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in play_buttons:
                        if button.is_displayed() and button.is_enabled():
                            button.click()
                            logger.info(f"点击播放按钮: {selector}")
                            play_clicked = True
                            time.sleep(3)  # 给视频加载时间
                            break
                    if play_clicked:
                        break
                except Exception as e:
                    continue
            
            if not play_clicked:
                logger.info("未找到可点击的播放按钮，尝试其他方法...")
                
                # 尝试通过JavaScript查找并点击播放按钮
                try:
                    js_script = """
                    // 查找所有可能的播放按钮
                    var playButtons = document.querySelectorAll('.play-btn, .video-play, .vjs-big-play-button, [class*="play"], button[title*="播放"], button[aria-label*="播放"]');
                    for (var i = 0; i < playButtons.length; i++) {
                        if (playButtons[i].offsetParent !== null && !playButtons[i].disabled) {
                            playButtons[i].click();
                            console.log('通过JS点击播放按钮');
                            return true;
                        }
                    }
                    
                    // 尝试点击视频区域
                    var videoElements = document.querySelectorAll('video, .video-js, .video-player, [class*="video"]');
                    for (var i = 0; i < videoElements.length; i++) {
                        if (videoElements[i].offsetParent !== null) {
                            videoElements[i].click();
                            console.log('点击视频区域');
                            return true;
                        }
                    }
                    
                    // 尝试通过事件触发播放
                    var videos = document.querySelectorAll('video');
                    for (var i = 0; i < videos.length; i++) {
                        if (videos[i].paused) {
                            videos[i].play();
                            console.log('通过play()方法播放视频');
                            return true;
                        }
                    }
                    
                    return false;
                    """
                    
                    result = self.driver.execute_script(js_script)
                    if result:
                        logger.info("通过JavaScript成功播放视频")
                        play_clicked = True
                        time.sleep(3)
                except Exception as e:
                    logger.warning(f"JavaScript播放视频失败: {e}")
            
            if play_clicked:
                logger.info("视频开始播放")
            else:
                logger.info("未找到播放按钮，可能视频已自动播放或需要手动操作")
                
        except Exception as e:
            logger.warning(f"播放视频时出错: {e}")
    
    def is_video_playing(self):
        """检查视频是否正在播放"""
        try:
            js_script = """
            // 查找视频元素
            var videos = document.querySelectorAll('video');
            for (var i = 0; i < videos.length; i++) {
                if (!videos[i].paused && videos[i].currentTime > 0) {
                    return true;  // 视频正在播放
                }
            }
            return false;  // 没有视频在播放
            """
            
            is_playing = self.driver.execute_script(js_script)
            return is_playing
            
        except Exception as e:
            logger.warning(f"检查视频状态时出错: {e}")
            return False
    
    def is_video_ended(self):
        """检查视频是否已播放结束（更严格的检查）"""
        try:
            js_script = """
            // 查找视频元素
            var videos = document.querySelectorAll('video');
            for (var i = 0; i < videos.length; i++) {
                var video = videos[i];
                
                // 确保视频有有效时长（大于10秒）
                if (video.duration <= 10) {
                    continue;  // 跳过时长太短的视频
                }
                
                // 检查视频是否已结束（currentTime >= duration - 1）
                // 使用更严格的条件：视频时长大于10秒，且播放进度超过95%
                if (video.duration > 10 && video.currentTime >= video.duration - 1) {
                    console.log('视频结束检测：时长=' + video.duration + ', 当前时间=' + video.currentTime);
                    return true;
                }
                
                // 检查视频的ended属性
                if (video.ended) {
                    console.log('视频结束检测：ended属性为true');
                    return true;
                }
            }
            
            // 检查是否有重播按钮（更严格的检查）
            var replayButtons = document.querySelectorAll('.replay-btn, .vjs-replay, [class*="replay"], button[title*="重播"], button[aria-label*="重播"]');
            for (var i = 0; i < replayButtons.length; i++) {
                var btn = replayButtons[i];
                // 确保按钮可见且包含"重播"文本
                if (btn.offsetParent !== null && 
                    (btn.textContent.includes('重播') || 
                     btn.getAttribute('title')?.includes('重播') ||
                     btn.getAttribute('aria-label')?.includes('重播'))) {
                    console.log('找到重播按钮：' + btn.textContent);
                    return true;
                }
            }
            
            // 检查结束画面（更严格的检查）
            var endScreens = document.querySelectorAll('.video-ended, .end-screen, .vjs-ended');
            for (var i = 0; i < endScreens.length; i++) {
                if (endScreens[i].offsetParent !== null) {
                    console.log('找到结束画面');
                    return true;
                }
            }
            
            return false;  // 视频未结束
            """
            
            is_ended = self.driver.execute_script(js_script)
            if is_ended:
                logger.debug("检测到视频已结束")
            return is_ended
            
        except Exception as e:
            logger.warning(f"检查视频是否结束时出错: {e}")
            return False
    
    def ensure_video_playing(self):
        """确保视频正在播放，如果不在播放则尝试播放"""
        # 先检查视频是否已结束
        if self.is_video_ended():
            logger.info("视频已结束，尝试播放下一个视频")
            if self.go_to_next_video():
                return
            else:
                logger.warning("无法播放下一个视频，尝试重新播放当前视频")
        
        # 检查视频是否在播放
        if not self.is_video_playing():
            logger.info("视频未在播放，尝试重新播放")
            self.play_video()
            time.sleep(3)
            
            # 再次检查
            if self.is_video_playing():
                logger.info("视频已成功重新播放")
            else:
                logger.warning("视频重新播放失败，可能需要手动操作")
    
    def check_for_questions(self):
        """检查是否有题目弹出"""
        try:
            # 常见的题目弹窗选择器
            question_selectors = [
                ".question-popup",
                ".exam-dialog",
                ".quiz-modal",
                ".test-modal",
                "[class*='question']",
                "[class*='exam']",
                "[class*='quiz']",
                "[class*='test']",
                ".dialog-content",
                ".modal-content",
                ".popup-content",
                ".question-dialog",
                ".exercise-popup"
            ]
            
            for selector in question_selectors:
                try:
                    question_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in question_elements:
                        if element.is_displayed():
                            logger.info(f"检测到题目弹窗，选择器: {selector}")
                            return True
                except:
                    continue
            
            # 检查是否有模态框
            try:
                modals = self.driver.find_elements(By.CSS_SELECTOR, ".modal, .dialog, .popup")
                for modal in modals:
                    if modal.is_displayed() and modal.value_of_css_property("display") != "none":
                        # 检查模态框内是否有题目相关文本
                        modal_text = modal.text.lower()
                        if any(keyword in modal_text for keyword in ["题目", "问题", "选择", "单选", "多选", "判断", "quiz", "question"]):
                            logger.info("检测到包含题目的模态框")
                            return True
            except:
                pass
            
            return False
            
        except Exception as e:
            logger.warning(f"检查题目时出错: {e}")
            return False
    
    def answer_question(self):
        """随机选择答案并提交"""
        logger.info("正在处理题目...")
        
        try:
            # 查找所有可能的答案选项
            answer_selectors = [
                ".answer-option",
                ".option-item",
                "[class*='option']",
                ".choice-item",
                ".select-item",
                "input[type='radio']",
                "input[type='checkbox']",
                ".radio-item",
                ".checkbox-item",
                ".question-option",
                ".quiz-option"
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
            
            # 随机选择一个或多个答案（如果是多选题）
            try:
                # 检查是否是多选题
                is_multiple = False
                checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                if checkboxes:
                    is_multiple = True
                
                if is_multiple:
                    # 多选题：随机选择1-3个答案
                    num_to_select = random.randint(1, min(3, len(answers)))
                    selected_answers = random.sample(answers, num_to_select)
                    for answer in selected_answers:
                        try:
                            answer.click()
                        except:
                            self.driver.execute_script("arguments[0].click();", answer)
                    logger.info(f"已选择 {num_to_select} 个答案（多选题）")
                else:
                    # 单选题：随机选择一个答案
                    selected_answer = random.choice(answers)
                    try:
                        selected_answer.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", selected_answer)
                    logger.info(f"已选择答案: {selected_answer.text[:50] if selected_answer.text else '无文本'}")
            except Exception as e:
                logger.warning(f"选择答案时出错: {e}")
                # 如果出错，尝试点击第一个答案
                try:
                    answers[0].click()
                    logger.info("已选择第一个答案")
                except:
                    return False
            
            time.sleep(1)
            
            # 查找并点击提交按钮
            submit_selectors = [
                ".submit-btn",
                ".confirm-btn",
                ".next-btn",
                "[class*='submit']",
                "[class*='confirm']",
                "[class*='next']",
                "button:contains('提交')",
                "button:contains('确定')",
                "button:contains('下一题')",
                "button:contains('继续')",
                "button:contains('完成')"
            ]
            
            submitted = False
            for selector in submit_selectors:
                try:
                    submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in submit_buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            logger.info("已提交答案")
                            submitted = True
                            time.sleep(2)
                            break
                    if submitted:
                        break
                except:
                    continue
            
            if not submitted:
                logger.warning("未找到提交按钮，尝试关闭弹窗")
                self.close_popup()
            
            # 答题后重新播放视频
            logger.info("答题完成，尝试重新播放视频")
            self.play_video()
            
            return True
            
        except Exception as e:
            logger.error(f"答题时出错: {e}")
            return False
    
    def go_to_next_video(self):
        """跳转到下一个视频"""
        logger.info("正在查找下一个视频按钮...")
        
        try:
            # 常见的下一个视频按钮选择器
            next_video_selectors = [
                ".next-btn",
                ".next-video",
                ".next-chapter",
                ".next-section",
                ".next-lesson",
                "[class*='next']",
                "button[title*='下一']",
                "button[aria-label*='下一']",
                ".vjs-next-button",
                ".video-next",
                ".course-next",
                ".study-next",
                ".continue-btn",
                ".continue-study",
                ".continue-learning",
                "button:contains('继续学习')",
                "button:contains('下一节')",
                "button:contains('下一个')",
                "button:contains('下一章')",
                "button:contains('继续')",
                ".next-page",
                ".next-step"
            ]
            
            next_clicked = False
            
            for selector in next_video_selectors:
                try:
                    next_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in next_buttons:
                        if button.is_displayed() and button.is_enabled():
                            button.click()
                            logger.info(f"点击下一个视频按钮: {selector}")
                            next_clicked = True
                            time.sleep(3)  # 给页面加载时间
                            break
                    if next_clicked:
                        break
                except Exception as e:
                    continue
            
            if not next_clicked:
                logger.info("未找到下一个视频按钮，尝试通过JavaScript查找...")
                
                # 尝试通过JavaScript查找并点击下一个按钮
                try:
                    js_script = """
                    // 查找所有可能的下一个按钮
                    var nextButtons = document.querySelectorAll('.next-btn, .next-video, [class*="next"], button[title*="下一"], button[aria-label*="下一"], .continue-btn, button:contains("继续学习"), button:contains("下一节")');
                    for (var i = 0; i < nextButtons.length; i++) {
                        if (nextButtons[i].offsetParent !== null && !nextButtons[i].disabled) {
                            nextButtons[i].click();
                            console.log('通过JS点击下一个视频按钮');
                            return true;
                        }
                    }
                    
                    // 尝试查找课程目录中的下一个项目
                    var courseItems = document.querySelectorAll('.course-item, .lesson-item, .video-item, [class*="item"]');
                    for (var i = 0; i < courseItems.length; i++) {
                        if (courseItems[i].classList.contains('active') || courseItems[i].classList.contains('current')) {
                            if (i + 1 < courseItems.length) {
                                courseItems[i + 1].click();
                                console.log('点击课程目录中的下一个项目');
                                return true;
                            }
                        }
                    }
                    
                    // 尝试查找进度条或导航中的下一个链接
                    var nextLinks = document.querySelectorAll('a[href*="next"], a:contains("下一"), .nav-next');
                    for (var i = 0; i < nextLinks.length; i++) {
                        if (nextLinks[i].offsetParent !== null) {
                            nextLinks[i].click();
                            console.log('点击下一个链接');
                            return true;
                        }
                    }
                    
                    return false;
                    """
                    
                    result = self.driver.execute_script(js_script)
                    if result:
                        logger.info("通过JavaScript成功跳转到下一个视频")
                        next_clicked = True
                        time.sleep(3)
                except Exception as e:
                    logger.warning(f"JavaScript跳转下一个视频失败: {e}")
            
            if next_clicked:
                logger.info("已跳转到下一个视频，等待页面加载...")
                time.sleep(5)  # 等待新页面加载
                
                # 尝试播放新视频
                logger.info("尝试播放新视频...")
                self.play_video()
                return True
            else:
                logger.warning("未找到下一个视频按钮，可能需要手动操作")
                return False
                
        except Exception as e:
            logger.error(f"跳转到下一个视频时出错: {e}")
            return False
    
    def close_popup(self):
        """关闭弹窗"""
        try:
            # 查找关闭按钮
            close_selectors = [
                ".close-btn",
                ".modal-close",
                ".dialog-close",
                ".popup-close",
                "[class*='close']",
                "button[aria-label='关闭']",
                ".icon-close",
                "button[title='关闭']",
                ".cancel-btn",
                ".btn-close"
            ]
            
            for selector in close_selectors:
                try:
                    close_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in close_buttons:
                        if btn.is_displayed():
                            btn.click()
                            logger.info("已关闭弹窗")
                            time.sleep(1)
                            return True
                except:
                    continue
            
            # 如果没有找到关闭按钮，尝试按ESC键
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            logger.info("已按ESC键关闭弹窗")
            time.sleep(1)
            
            # 关闭弹窗后尝试重新播放视频
            logger.info("弹窗关闭，尝试重新播放视频")
            self.play_video()
            
            return True
            
        except Exception as e:
            logger.warning(f"关闭弹窗时出错: {e}")
            return False
    
    def monitor_course(self, duration_minutes=60, manual_mode=False):
        """
        监控课程进度
        
        Args:
            duration_minutes: 监控时长（分钟）
            manual_mode: 是否手动模式（用户先手动选择视频）
        """
        if manual_mode:
            logger.info("手动模式：请先手动选择并播放第一个视频")
            print("\n" + "=" * 60)
            print("手动模式说明:")
            print("1. 请手动选择要刷的视频")
            print("2. 手动点击播放按钮开始播放")
            print("3. 脚本将自动处理题目和播放下一个视频")
            print("=" * 60 + "\n")
            input("准备好后按回车键开始自动化监控...")
            logger.info("开始自动化监控（手动模式）")
        else:
            logger.info(f"开始监控课程，时长: {duration_minutes}分钟")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        question_count = 0
        video_count = 1  # 当前播放的视频计数
        last_check_time = time.time()
        last_video_end_check = time.time()
        last_status_time = time.time()
        
        # 在手动模式下，不自动播放第一个视频
        if not manual_mode:
            logger.info("尝试播放第一个视频...")
            self.play_video()
            time.sleep(5)  # 给视频加载时间
        
        while time.time() < end_time:
            try:
                current_time = time.time()
                
                # 每20秒检查一次题目（比之前慢一点，减少误判）
                if current_time - last_check_time > 20:
                    if self.check_for_questions():
                        logger.info(f"检测到第{question_count + 1}个题目")
                        if self.answer_question():
                            question_count += 1
                        time.sleep(3)  # 给答题和弹窗关闭留出时间
                    
                    # 检查视频状态（但不自动播放，避免干扰手动操作）
                    if not self.is_video_playing() and not manual_mode:
                        logger.info("视频未在播放，尝试重新播放")
                        self.play_video()
                        time.sleep(3)
                    
                    last_check_time = current_time
                
                # 每15秒检查一次视频是否结束（比之前慢一点）
                if current_time - last_video_end_check > 15:
                    if self.is_video_ended():
                        logger.info(f"视频 {video_count} 播放结束，尝试播放下一个视频")
                        
                        # 等待更长时间，确保视频完全结束
                        time.sleep(3)
                        
                        # 尝试跳转到下一个视频
                        if self.go_to_next_video():
                            video_count += 1
                            logger.info(f"开始播放第 {video_count} 个视频")
                            time.sleep(5)  # 给新视频页面加载时间
                            
                            # 尝试播放新视频
                            if not manual_mode:
                                self.play_video()
                                time.sleep(3)
                        else:
                            logger.info("未找到下一个视频，可能已到课程末尾")
                            # 如果无法跳转，等待一段时间再检查
                            time.sleep(10)
                    
                    last_video_end_check = current_time
                
                # 每60秒记录一次状态（比之前慢一点）
                if current_time - last_status_time > 60:
                    elapsed_minutes = int((current_time - start_time) / 60)
                    remaining_minutes = int((end_time - current_time) / 60)
                    logger.info(f"已运行 {elapsed_minutes} 分钟，剩余 {remaining_minutes} 分钟")
                    logger.info(f"播放了 {video_count} 个视频，处理了 {question_count} 个题目")
                    last_status_time = current_time
                
                # 短暂休眠避免CPU占用过高
                time.sleep(3)
                
            except KeyboardInterrupt:
                logger.info("用户中断监控")
                break
            except Exception as e:
                logger.error(f"监控过程中出错: {e}")
                time.sleep(10)  # 出错后等待更长时间
        
        logger.info(f"监控结束，总共播放了 {video_count} 个视频，处理了 {question_count} 个题目")
    
    def run(self, duration_minutes=60, manual_mode=False):
        """运行自动化刷课
        
        Args:
            duration_minutes: 刷课时长（分钟）
            manual_mode: 是否手动模式（用户先手动选择视频）
        """
        try:
            # 显示浏览器信息
            logger.info(f"使用浏览器: {self.browser_type.value}")
            logger.info(f"目标平台: {self.platform_configs[self.platform_type]['name']}")
            
            # 登录（如果需要）
            self.login()
            
            # 导航到课程（带重试机制）
            if not self.navigate_to_course():
                logger.error("课程页面加载失败")
                print("\n⚠️  课程页面加载失败，可能原因:")
                print("1. 网络连接问题")
                print("2. 课程URL错误")
                print("3. 需要登录验证")
                print("4. 网站访问限制")
                print("\n请检查:")
                print(f"- 课程URL: {self.course_url}")
                print("- 网络连接是否正常")
                print("- 是否已登录平台")
                
                # 询问用户是否继续
                continue_anyway = input("\n是否继续尝试？(y/n): ").strip().lower()
                if continue_anyway != 'y':
                    logger.info("用户选择停止")
                    return
            
            # 显示当前页面状态
            try:
                current_url = self.driver.current_url
                page_title = self.driver.title
                logger.info(f"当前页面:")
                logger.info(f"  URL: {current_url}")
                logger.info(f"  标题: {page_title}")
                
                # 检查是否在正确的页面
                if self.course_url not in current_url:
                    logger.warning(f"当前页面与目标URL不匹配")
                    logger.warning(f"目标: {self.course_url}")
                    logger.warning(f"实际: {current_url}")
            except:
                pass
            
            # 开始监控（根据模式决定是否自动播放）
            self.monitor_course(duration_minutes, manual_mode)
            
        except KeyboardInterrupt:
            logger.info("用户中断程序")
        except Exception as e:
            logger.error(f"运行过程中发生错误: {e}")
            import traceback
            logger.error(f"错误详情:\n{traceback.format_exc()}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        logger.info("正在关闭浏览器...")
        try:
            self.driver.quit()
            logger.info("浏览器已关闭")
        except:
            pass

def main():
    """主函数"""
    print("=" * 60)
    print("跨平台刷课自动化系统")
    print("支持: Chrome, Firefox, Edge, Safari")
    print("=" * 60)
    
    # 获取用户输入
    course_url = input("请输入课程页面URL: ").strip()
    
    print("\n选择刷课平台:")
    print("1. 智慧树 (zhihuishu.com)")
    print("2. 超星学习通 (chaoxing.com)")
    print("3. 知到 (zhihuishu.com)")
    print("4. 其他平台")
    
    platform_choice = input("请输入选项 (1-4) [默认1]: ").strip() or "1"
    
    platform_map = {
        "1": PlatformType.ZHIHUISHU,
        "2": PlatformType.CHAOXING,
        "3": PlatformType.ZHIDAO,
        "4": PlatformType.OTHER
    }
    
    platform_type = platform_map.get(platform_choice, PlatformType.ZHIHUISHU)
    
    print("\n选择浏览器:")
    print("1. Chrome (推荐)")
    print("2. Firefox")
    print("3. Edge")
    print("4. Safari (仅macOS)")
    
    browser_choice = input("请输入选项 (1-4) [默认1]: ").strip() or "1"
    
    browser_map = {
        "1": BrowserType.CHROME,
        "2": BrowserType.FIREFOX,
        "3": BrowserType.EDGE,
        "4": BrowserType.SAFARI
    }
    
    browser_type = browser_map.get(browser_choice, BrowserType.CHROME)
    
    use_headless = input("是否使用无头模式？(y/n) [默认n]: ").strip().lower() or "n"
    headless = use_headless == 'y'
    
    use_login = input("是否需要自动登录？(y/n): ").strip().lower()
    
    username = None
    password = None
    
    if use_login == 'y':
        username = input("请输入用户名: ").strip()
        password = input("请输入密码: ").strip()
    
    try:
        duration = int(input("请输入刷课时长（分钟）[默认60]: ").strip() or "60")
    except ValueError:
        duration = 60
    
    print("\n选择操作模式:")
    print("1. 自动模式 - 脚本自动播放第一个视频")
    print("2. 手动模式 - 用户先手动选择并播放视频（推荐）")
    
    mode_choice = input("请输入选项 (1-2) [默认2]: ").strip() or "2"
    manual_mode = mode_choice == "2"
    
    print("\n" + "=" * 60)
    print("配置信息:")
    print(f"课程URL: {course_url}")
    print(f"平台: {platform_type.value}")
    print(f"浏览器: {browser_type.value}")
    print(f"操作模式: {'手动模式' if manual_mode else '自动模式'}")
    print(f"无头模式: {'是' if headless else '否'}")
    print(f"刷课时长: {duration}分钟")
    if username:
        print(f"用户名: {username}")
    print("=" * 60 + "\n")
    
    confirm = input("确认开始刷课？(y/n): ").strip().lower()
    
    if confirm != 'y':
        print("已取消")
        return
    
    # 创建并运行自动化工具
    auto_course = CrossPlatformCourseAutomation(
        course_url, 
        browser_type, 
        platform_type,
        username, 
        password, 
        headless
    )
    
    try:
        auto_course.run(duration, manual_mode)
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"程序运行出错: {e}")
    finally:
        auto_course.cleanup()

if __name__ == "__main__":
    main()