# -*- encoding=utf8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from utils.utils import locate_web_driver

with open('stealth.min.js') as f:
    js = f.read()


class ChromeDriver:
    def __init__(self, is_headless):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--incognito')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-logging")
        options.add_argument('--log-level=2')
        options.add_argument('--disable-gpu')
        if is_headless == 1: options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=locate_web_driver(), options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        self.init_web()

    def init_web(self):
        self.get_web("https://www.baidu.com", 0)

    def close(self):
        try:
            self.driver.quit()
        except:
            pass

    def get_web(self, url, second=3):
        self.driver.get(url)
        time.sleep(second)

    def send_text(self, xpath, text="", second=1):
        self.get_element(xpath).send_keys(text)
        time.sleep(second)

    def click(self, xpath, second=1):
        self.execute_script("arguments[0].click()", self.get_element(xpath), second)

    def set_cookie(self, url, cookie):
        domain = urlparse(url).netloc.replace("www.", "")
        cookie = {c.split("=", 1)[0]: c.split("=", 1)[1] for c in cookie.strip().split("; ")}
        cookies = [
            {"name": key, "value": value.strip().strip(";"), "path": "/", "domain": ".{}".format(domain)}
            for key, value in cookie.items()
        ]
        self.driver.delete_all_cookies()
        time.sleep(0.5)
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def wait_element(self, xpath):
        try:
            ele = WebDriverWait(self.driver, 25, 1).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return ele
        except:
            return False

    def execute_script(self, script, cla=None, second=0):
        self.driver.execute_script(script, cla) if cla else self.driver.execute_script(script)
        time.sleep(second)

    def get_element(self, xpath, second=5):
        elements = self.driver.find_elements_by_xpath(xpath)
        if elements: return elements[0]
        last_time = int(time.time()) + second
        while int(time.time()) < last_time:
            elements = self.driver.find_elements_by_xpath(xpath)
            if elements: return elements[0]
