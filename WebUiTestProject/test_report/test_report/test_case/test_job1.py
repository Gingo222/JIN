# -*- coding: utf-8 -*-

import unittest
import time
from selenium import webdriver


class JobTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.url = 'http://10.25.84.86:8080/index.html'
        self.pic_path = 'picture/'

    def test_Login(self):
        browser = self.driver
        browser.get(self.url)
        browser.maximize_window()
        browser.find_element_by_xpath("/html/body/div[3]/div[3]/form/div[1]/input").send_keys("jinjie674")
        browser.find_element_by_xpath("/html/body/div[3]/div[3]/form/div[2]/input").send_keys("1111aaaa")
        browser.find_element_by_xpath("/html/body/div[3]/div[3]/form/div[3]/a").click()
        time.sleep(3)
        if (browser.find_element_by_xpath("/html/body/div[4]/div[2]/div[1]").text).encode('utf-8') == "用户名或密码错误":
            current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            browser.save_screenshot(self.pic_path + str(current_time) + '.png')
            self.assertEqual("pass", "fail")
        self.assertEqual("pass", "pass")
        return


    def tearDown(self):
        self.driver.close()
        self.driver.quit()