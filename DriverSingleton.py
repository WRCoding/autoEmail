from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

import config

prefs = {
    "download.default_directory": config.get_location(),
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

chrome_option = Options()
chrome_option.add_experimental_option('prefs', prefs)


class DriverSingleton:
    _instance = None
    _driver: WebDriver = None
    _wait = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DriverSingleton, cls).__new__(cls)
            cls._driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_option)  # 或者你选择的浏览器
            cls._wait = WebDriverWait(cls._driver, 360)  # 可以调整等待时间
        return cls._instance

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls()
        return cls._driver

    @classmethod
    def get_wait(cls):
        if cls._wait is None:
            cls()
        return cls._wait

    @classmethod
    def init(cls):
        if cls._driver is None or cls._wait is None:
            cls()
        return cls._driver, cls._wait
