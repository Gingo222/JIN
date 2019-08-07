# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver


class CTest(unittest.TestCase):

    _url = 'http://103.211.47.130:72'
    driver = None

    @staticmethod
    def setUpClass(cls):
        if cls.driver is None:
            cls.driver = webdriver.Chrome()
            driver = cls.driver

    def test_login(self):
        # 登录
        driver.find_element_by_xpath('//*[@id="userName"]').send_keys('jinjie')
        driver.find_element_by_xpath('//*[@id="password"]').send_keys('123456')
        driver.find_element_by_xpath('//*[@id="content"]/div/div/main/div/div/div/div[2]/form/div[3]'
                                          '/div/div/span/button').click()

    def test_operate(self):
        list_common_part = '//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/' \
                           'div/div/div/div/div/table/tbody/tr['
        list_operate = ']/td[10]/button'
        self.driver.find_element_by_xpath(list_common_part + list_operate).click()

