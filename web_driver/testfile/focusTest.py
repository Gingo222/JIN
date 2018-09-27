# -*- coding: utf-8 -*-

import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from pymouse import PyMouseEvent

reload(sys)
sys.setdefaultencoding('utf-8')


class CtaReport(object):

    _url = 'http://103.211.47.130:74'
    _driver = '../chrome_driver/chromedriver'
    _chrome_options = Options()
    _chrome_options.add_argument('--headless')
    _chrome_options.add_argument('--disable-gpu')
    _chrome_options.add_argument('--no-sandbox')
    _errorList = []

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CtaReport._driver)
        self.driver.get(CtaReport._url)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        # 登录
        self.driver.find_element_by_xpath('//*[@id="userName"]').send_keys('jinjie')
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div/main/div/div/div/div[2]/form/div[3]'
                                          '/div/div/span/button').click()
        time.sleep(3)

    def operate_in(self):
        operate_button = '//*[@id="content"]/div/div/div/div/div[1]/div/div/div/div/table/tbody/tr[1]/td[13]/button'
        self.driver.find_element_by_xpath(operate_button).click()
        time.sleep(5)

    @staticmethod
    def runner():
        CtaReport.operate_in()
        CtaReport.compare_report()
        CtaReport.finally_done()

    def finally_done(self):
        self.driver.quit()

    def compare_report(self):
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="content"]/div/div/section/div/div[2]/div[1]/div').click()
        m = PyMouse()
        k = PyKeyboard()
        r = PyMouse.scroll(vertical=0, horizontal=0, depth=-1)
        PyMouseEvent()



if __name__ == '__main__':
    CtaReport = CtaReport()
    CtaReport.runner()