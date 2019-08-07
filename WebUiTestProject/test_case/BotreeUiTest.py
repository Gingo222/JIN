# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from CypressUiTest import ReuseChrome
import HTMLTestRunner
import random


class BoTreeUiTest(unittest.TestCase):

    _url = "http://103.211.47.130:72"
    _sessionId_file = '../sessionId/sessionId.txt'
    _executor_url_file = '../executor_url/executor_url.txt'
    _current_url_file = '../executor_url/current_url.txt'

    def setUp(self):
        with open(BoTreeUiTest._sessionId_file)as session_file:
            if session_file.read():
                session_file = open(BoTreeUiTest._sessionId_file)
                session_id = session_file.read()
                session_file.close()
                executor_url_file = open(BoTreeUiTest._executor_url_file)
                executor_url = executor_url_file.read()
                executor_url_file.close()
                self.driver = ReuseChrome(command_executor=executor_url, session_id=session_id)
                self.driver.get(BoTreeUiTest._url)
            else:
                self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)

    @classmethod
    def setUpClass(cls):
        print("test class start =======>")

    def test_login(self):
        self.driver.get(BoTreeUiTest._url)
        self.driver.find_element_by_xpath('//*[@id="userName"]').send_keys('jinjie')
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div/main/div/div/div/div[2]/form/div[3]'
                                          '/div/div/span/button').click()
        return

    def test_operate_button(self):
        operate_Button = '//*[@id="content"]/div/div/div/div/div[1]/div/div/div/div/table/tbody/tr[1]/td[13]/button'
        axial_pic_path = ''
        d3_pic_path = ''
        cpr_pic_path = ''
        section_pic_path = ''
        if self.driver.find_element_by_xpath(operate_Button):
            self.driver.find_element_by_xpath(operate_Button).click()
        else:
            return

    def picture_operate(self):
        pass

    @staticmethod
    def del_file_info():
        with open(BoTreeUiTest._sessionId_file, 'r+')as s:
            s.write('')
        with open(BoTreeUiTest._current_url_file, 'r+')as c:
            c.write('')
        with open(BoTreeUiTest._executor_url_file, 'r+')as e:
            e.write('')


