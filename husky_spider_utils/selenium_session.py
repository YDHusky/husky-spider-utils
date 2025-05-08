import json
import os
import random
import shutil
import time

import requests
from selenium import webdriver
from loguru import logger
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from parsel import Selector


class SeleniumSession:
    driver = None
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    def __init__(self, selenium_init_url="https://cn.bing.com", driver_type="firefox", headers=None, download_path="",
                 driver_path="./", os_type="windows", option=None):
        self.download_path = download_path
        self.option = option
        self.driver_path = driver_path
        self.os_type = os_type
        self.init_headers(headers)
        self.init_driver(driver_type)
        self.selenium_get(selenium_init_url)

    def init_headers(self, headers):
        logger.debug("初始化请求头中...")
        if headers is not None:
            self.headers.update(headers)

    def init_driver(self, driver_type):
        match driver_type:
            case "firefox":
                option = webdriver.FirefoxOptions()
                if self.option is not None:
                    option = self.option
                self.driver_path += os.path.join(self.driver_path, "geckodriver")
                if self.os_type == "windows":
                    self.driver_path += ".exe"
                    if not os.path.exists(os.path.join(self.driver_path)):
                        driver_path = GeckoDriverManager().install()
                        shutil.copy(driver_path, os.path.join(self.driver_path))
                if self.os_type == "linux":
                    if not os.path.exists(os.path.join(self.driver_path)):
                        driver_path = ChromeDriverManager().install()
                        shutil.copy(driver_path, os.path.join(self.driver_path))
                if os.path.exists(self.download_path) and self.download_path != "":
                    option.set_preference("browser.download.folderList", 2)
                    option.set_preference('browser.download.manager.showWhenStarting', False)
                    option.set_preference("browser.download.dir", self.download_path)
                logger.debug("加载浏览器firefox...")
                from selenium.webdriver.firefox.service import Service
                self.driver = webdriver.Firefox(service=Service(executable_path=self.driver_path), options=option)
            case "chrome":
                prefs = {
                    "profile.default_content_setting_values.automatic_downloads": 1  # 允许多文件下载
                }
                if os.path.exists(self.download_path) and self.download_path != "":
                    prefs.update({
                        'download.default_directory': rf"{self.download_path}",  # 设置默认下载路径
                    })
                option = webdriver.ChromeOptions()
                if self.option is not None:
                    option = self.option
                option.add_experimental_option("prefs", prefs)
                self.driver_path += os.path.join(self.driver_path, "chromedriver")
                if self.os_type == "windows":
                    self.driver_path += ".exe"
                    if not os.path.exists(os.path.join(self.driver_path)):
                        driver_path = ChromeDriverManager().install()
                        shutil.copy(driver_path, os.path.join(self.driver_path))
                if self.os_type == "linux":
                    if not os.path.exists(os.path.join(self.driver_path)):
                        driver_path = ChromeDriverManager().install()
                        shutil.copy(driver_path, os.path.join(self.driver_path))
                logger.debug("加载浏览器chrome...")
                from selenium.webdriver.chrome.service import Service
                self.driver = webdriver.Chrome(service=Service(executable_path=self.driver_path), options=option)
            case "edge":
                prefs = {
                    "profile.default_content_setting_values.automatic_downloads": 1  # 允许多文件下载
                }
                if os.path.exists(self.download_path) and self.download_path != "":
                    prefs.update({
                        'download.default_directory': rf"{self.download_path}",  # 设置默认下载路径
                    })
                option = webdriver.EdgeOptions()
                if self.option is not None:
                    option = self.option
                option.add_experimental_option("prefs", prefs)
                self.driver_path += os.path.join(self.driver_path, "edgedriver")
                if self.os_type == "windows":
                    self.driver_path += ".exe"
                    if not os.path.exists(os.path.join(self.driver_path)):
                        driver_path = EdgeChromiumDriverManager().install()
                        shutil.copy(driver_path, os.path.join(self.driver_path))
                if self.os_type == "linux":
                    if not os.path.exists(os.path.join(self.driver_path)):
                        driver_path = EdgeChromiumDriverManager().install()
                        shutil.copy(driver_path, os.path.join(self.driver_path))
                logger.debug("加载浏览器edge...")

                from selenium.webdriver.edge.service import Service
                self.driver = webdriver.Edge(service=Service(executable_path=self.driver_path), options=option)
            case _:
                option = webdriver.FirefoxOptions()
                if self.option is not None:
                    option = self.option
                self.driver_path += os.path.join(self.driver_path, "geckodriver")
                if self.os_type == "windows":
                    self.driver_path += ".exe"
                    if not os.path.exists(os.path.join(self.driver_path)):
                        driver_path = GeckoDriverManager().install()
                        shutil.copy(driver_path, os.path.join(self.driver_path))
                if self.os_type == "linux":
                    if not os.path.exists(os.path.join(self.driver_path)):
                        driver_path = ChromeDriverManager().install()
                        shutil.copy(driver_path, os.path.join(self.driver_path))
                if os.path.exists(self.download_path) and self.download_path != "":
                    option.set_preference("browser.download.folderList", 2)
                    option.set_preference('browser.download.manager.showWhenStarting', False)
                    option.set_preference("browser.download.dir", self.download_path)
                logger.debug("加载浏览器firefox...")
                from selenium.webdriver.firefox.service import Service
                self.driver = webdriver.Firefox(service=Service(executable_path=self.driver_path), options=option)

    def get(self, url, headers=None, is_to_driver=True, is_refresh=True, **kwargs):
        header_data = self.headers.copy()
        if headers is not None:
            header_data.update(headers)

        logger.debug(f"session请求(method: GET): {url}")

        res = self.session.get(url, headers=header_data, **kwargs)
        if is_to_driver:
            self.cookies_to_driver(is_refresh=is_refresh)
        return res

    def get_img_base64_from_img_tag(self, value, by=By.CSS_SELECTOR, timeout=60):
        js_code = """
                   const canvas = document.createElement('canvas');
                   canvas.width = arguments[0].width;
                   canvas.height = arguments[0].height;
                   const context = canvas.getContext('2d');
                   context.drawImage(arguments[0], 0, 0);
                   return canvas.toDataURL('image/png').split(',')[1];
                   """
        img = self.find_element(value, by=by, timeout=timeout)
        return self.execute_script(js_code, img)

    def get_action_chains(self):
        return ActionChains(self.driver)

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def find_element(self, value, by=By.CSS_SELECTOR, timeout=60):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"未能找到元素{value}")

    def post(self, url, data=None, json=None, headers=None, is_to_driver=True, is_refresh=True, **kwargs):
        header_data = self.headers.copy()
        if headers is not None:
            header_data.update(headers)
        logger.debug(f"session请求(method: POST): {url}")
        res = self.session.post(url, data=data, json=json, headers=header_data, **kwargs)
        if is_to_driver:
            self.cookies_to_driver(is_refresh=is_refresh)
        return res

    def request(self, url, method, headers=None, is_to_driver=True, is_refresh=True, **kwargs):
        header_data = self.headers.copy()
        if headers is not None:
            header_data.update(headers)
        logger.debug(f"session请求(method: {method}): {url}")
        res = self.session.request(method=method, url=url, headers=header_data, **kwargs)
        if is_to_driver:
            self.cookies_to_driver(is_refresh=is_refresh)
        return res

    def get_session_cookies_to_dict(self):
        cookies = self.session.cookies.get_dict()
        selenium_cookies = []
        for k, v in cookies.items():
            selenium_cookies.append({
                "name": k,
                "value": v,
            })
        return selenium_cookies

    def cookies_to_driver(self, is_refresh=True):
        for i in self.get_session_cookies_to_dict():
            self.driver.add_cookie(i)
        if is_refresh:
            self.driver.refresh()

    def selenium_get(self, url):
        logger.debug(f"浏览器请求: {url}")
        self.driver.get(url)
        self.selenium_cookies_to_session()
        self.driver.implicitly_wait(60)

    def selenium_cookies_to_session(self):
        for cookie in self.driver.get_cookies():
            self.session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"], path=cookie["path"])

    def send_key(self, value, send_value, by=By.CSS_SELECTOR, timeout=60):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        ).send_keys(send_value)

    def click(self, value, by=By.CSS_SELECTOR, timeout=60):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        ).click()

    def clean_key(self, value, by=By.CSS_SELECTOR, timeout=60):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        ).clear()

    def get_current_url(self):
        return self.driver.current_url

    def try_click(self, value, by=By.CSS_SELECTOR, timeout=60, max_attempt=0, sleep_time=0.5):
        """
        :param sleep_time: 尝试间隔时间
        :param value:
        :param by:
        :param timeout:
        :param max_attempt: 最大尝试次数
        :return:
        """
        attempt = 0
        while (attempt < max_attempt) or max_attempt == 0:
            attempt += 1
            logger.info(f"第{attempt}次尝试点击中...")
            try:
                self.click(value, by=by, timeout=timeout)
                logger.success("尝试点击成功!")
                return
            except Exception as e:
                logger.warning(f"第{attempt}次尝试点击失败!将在{sleep_time}s后尝试下一次点击! {e}")
                time.sleep(sleep_time)
        logger.error("尝试点击失败!")

    def try_send_key(self, value, send_value, by=By.CSS_SELECTOR, timeout=60, max_attempt=0, sleep_time=0.5):
        attempt = 0
        while (attempt < max_attempt) or max_attempt == 0:
            attempt += 1
            logger.info(f"第{attempt}次尝试发送中...")
            try:
                self.send_key(value, send_value=send_value, by=by, timeout=timeout)
                logger.success("尝试发送成功!")
                return
            except Exception as e:
                logger.warning(f"第{attempt}次尝试发送失败!将在{sleep_time}s后尝试下一次发送! {e}")
                time.sleep(sleep_time)
        logger.error("尝试发送失败!")

    def try_clean_key(self, value, by=By.CSS_SELECTOR, timeout=60, max_attempt=0, sleep_time=0.5):
        attempt = 0
        while (attempt < max_attempt) or max_attempt == 0:
            attempt += 1
            logger.info(f"第{attempt}次尝试清空中...")
            try:
                self.clean_key(value, by=by, timeout=timeout)
                logger.success("尝试清空成功!")
                return
            except Exception as e:
                logger.warning(f"第{attempt}次尝试清空失败!将在{sleep_time}s后尝试下一次清空! {e}")
                time.sleep(sleep_time)
        logger.error("尝试清空失败!")

    @staticmethod
    def sleep_random_time(min_time=5, max_time=10):
        random_time = random.randint(min_time, max_time)
        time.sleep(random_time)

    def hover(self, value, by=By.CSS_SELECTOR, timeout=60):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        ActionChains(self.driver).move_to_element(element).perform()

    def get_page_source(self):
        return self.driver.page_source

    def get_element_selector(self, value, by=By.CSS_SELECTOR, timeout=60):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        dom = Selector(text=self.get_page_source())
        match by:
            case By.CSS_SELECTOR:
                return dom.css(value)
            case By.XPATH:
                return dom.xpath(self.get_page_source())
            case By.ID:
                return dom.css(f"#{value}")
            case By.TAG_NAME:
                return dom.css(f"{value}")
            case _:
                return dom.css(value)

    @staticmethod
    def on_input(des=""):
        return input(des)

    def scroll(self, height=200):
        self.driver.execute_script("window.scrollTo(0, {})".format(height))

    def scroll_to_el(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_to_el_by_value(self, value, by=By.CSS_SELECTOR):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(by, value))

    def scroll_to_top(self):
        self.driver.execute_script("var q=document.documentElement.scrollTop=0")

    def scroll_to_bottom_fade(self, step=100, max_height=None):
        """
        平滑滚动页面到底部。

        通过逐步增加滚动距离，模拟用户手动滚动的效果。
        每次滚动的距离由 `step` 参数控制，默认为 100 像素。
        可以通过 `max_height` 参数指定最大滚动高度，如果未指定，则滚动到页面底部。

        :param step: 每次滚动的距离（像素），默认为 100。
        :param max_height: 最大滚动高度（像素），默认为页面底部。
        """
        if max_height is None:
            # 如果未指定最大高度，则获取页面的总高度
            max_height = self.driver.execute_script("return document.body.scrollHeight;")

        current_height = 0
        while current_height < max_height:
            # 每次滚动指定的距离
            self.driver.execute_script(f"window.scrollTo(0, {current_height});")
            current_height += step
            # 稍作停顿以实现平滑滚动效果
            self.driver.implicitly_wait(0.1)

    def scroll_to_bottom(self):
        """
        直接到达底部
        :return:
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def quit(self):
        """
        退出浏览器
        :return:
        """
        self.driver.quit()

    def save_cookies(self, save_path):
        logger.info(f"正在保存cookie中...")
        with open(save_path, "w") as f:
            f.write(json.dumps(self.driver.get_cookies()))

    def load_cookies(self, load_path):
        if os.path.exists(load_path):
            logger.info(f"找到{load_path}, 正在加载cookie中...")
            with open(load_path, "r") as f:
                cookies = json.loads(f.read())
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                    self.session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"],
                                             path=cookie["path"])
                self.driver.refresh()
