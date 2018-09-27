# -*- coding: utf-8 -*-
import sys
sys.path.append('../../')
reload(sys)


import ConfigParser
from selenium.webdriver.common.by import By
from daphne.mainrunner import DriverRunner
from daphne.func2.create_report import *


login_xpath_element_dict = {
    'userName': '//*[@id="userName"]',
    'password': '//*[@id="password"]',
    'button': '//*[@id="content"]/div/div/main/div/div/div/div[2]'
              '/form/div[3]/div/div/span/button'
    }


class LoginPage(DriverRunner):

    configParser = ConfigParser.ConfigParser()
    configParser.read('../config/config.ini')
    name = configParser.get('user', 'name')
    password = configParser.get('user', 'password')

    def __init__(self):
        super(LoginPage, self).__init__()
        self.driver.get(LoginPage.configParser.get('baseUrl', 'url') +
                        LoginPage.configParser.get('choose', 'id'))
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.username_xpath = (By.XPATH, login_xpath_element_dict['userName'])
        self.password_xpath = (By.XPATH, login_xpath_element_dict['password'])
        self.button_xpath = (By.XPATH, login_xpath_element_dict['button'])
        self.create_report_head = head()
        self.login_driver = self.find_element_xpath()

    def find_element_xpath(self):
        try:
            self.driver.find_element(*self.username_xpath).send_keys(LoginPage.name)
            self.driver.find_element(*self.password_xpath).send_keys(LoginPage.password)
            self.driver.find_element(*self.button_xpath).click()
            print(self.driver.page_source)
            part(u"登录页", u"登陆是否成功", "", "success", "")
            print("登录成功")
        except Exception as e:
            print(e)
            self.driver.quit()
            part(u"登录页", u"登陆是否成功", "", "fail", "no such element login fail")
            return False
        else:
            driver = self.driver
            return driver


if __name__ == '__main__':
    loginPage = LoginPage()
