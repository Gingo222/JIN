# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverRunner(object):
    _chrome_options = Options()
    _chrome_options.add_argument('--headless')
    _chrome_options.add_argument('--disable-gpu')
    _chrome_options.add_argument('--no-sandbox')
    _chrome_options.add_argument('–start-maximized')

    def __init__(self):
        self.driverPath = '../../chrome_driver/chromedriver'
        # self.display = Display(visible=0, size=(1100, 700))
        # self.display.start()
        self.driver = webdriver.Chrome(executable_path=self.driverPath,
                                       chrome_options=DriverRunner._chrome_options)
        self.driver.implicitly_wait(30)

    def is_element_exist(self, element, key_path):
        try:
            if key_path == 'xpath':
                self.driver.find_element_by_xpath(element)
                return True
            elif key_path == 'css_select':
                self.driver.find_element_by_css_selector(element)
                return True
        except:
            return False

    @staticmethod
    def runner():
        pass
