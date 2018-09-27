# -*- coding: utf-8 -*-
import ConfigParser
import time
from loginPage import LoginPage
from daphne.util.myutil import MysqlConnect
from daphne.util.sql.sql import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from daphne.func2.create_report import *


class ListPage(LoginPage, MysqlConnect):

    configParser = ConfigParser.ConfigParser()
    configParser.read('../config/config.ini')

    def __init__(self):
        LoginPage.__init__(self)
        MysqlConnect.__init__(self)
        self.choose_name = ListPage.configParser.get('choose', 'name')

    def judge_status(self):
        # search_xpath = '//*[@id="content"]/div/div/header/div[3]/span/input'
        # search_xpath_2 = u"(.//*[normalize-space(text()) and normalize-space(.)='全部影像'])[1]/following::input[1]"
        line_one_xpath = '//*[@id="content"]/div/div/div/div/div[1]/div/div/div/div/div[2]/table/tbody/tr/td[7]'
        line_one_id = '//*[@id="content"]/div/div/div/div/div[1]/div/div/div/div/div[2]/table/tbody/tr/td[5]'
        select_user_state_sql = select_user_state(self.choose_name)
        state = self.execute_select_status_sql(select_user_state_sql, kind='select_state')
        if state:
            if state != 2:
                update_user_state_sql = update_user_state(self.choose_name)
                self.execute_update_state_sql(update_user_state_sql)
                self.driver.refresh()
            time.sleep(2)

            # self.driver.find_element_by_xpath(search_xpath).click()
            # self.driver.find_element_by_xpath(search_xpath_2).send_keys(
            #    int(ListPage.configParser.get('choose', 'id')))
            # time.sleep(1)
            # 判断搜索是否成功
            if self.driver.find_element_by_xpath(line_one_id).text == ListPage.configParser.get('choose', 'id'):
                part(u"列表页", u"搜索是否成功", "", "success", "")
            else:
                part(u"列表页", u"搜索是否成功", "", "fail", u"未找到相应搜索的id" +
                     ListPage.configParser.get('choose', 'id'))
            time.sleep(1)
            WebDriverWait(self.driver, 100).until((
                lambda wait: self.driver.find_element_by_xpath(line_one_xpath)))
            line_one_xpath_obj = self.driver.find_element_by_xpath(line_one_xpath)
            action_chains = ActionChains(self.driver)
            action_chains.move_to_element(line_one_xpath_obj).click()
            action_chains.perform()
            part(u"列表页", u"点击病例跳转是否成功", "", "success", "")
            time.sleep(5)
            print(u"进入冠脉诊断页成功")
            return True
        else:
            return part(u"列表页", u"数据有问题", "", "fail", u"请查看配置文件是否准确")

