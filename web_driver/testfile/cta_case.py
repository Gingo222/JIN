# -*- coding: utf-8 -*-

import time
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from web_driver.test_case import data

reload(sys)
sys.setdefaultencoding('utf-8')


class CTA(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'http://103.211.47.130:70/'
        self.pic_path = '../picture/'
        self.driver.implicitly_wait(15)
        self.sessionId = self.driver.session_id

    def test_login(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        # 登录
        self.driver.find_element_by_xpath('//*[@id="userName"]').send_keys('jinjie')
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div/main/div/div/div/div[2]/form/div[3]'
                                          '/div/div/span/button').click()
        print(self.sessionId)
        time.sleep(3)
        if self.driver.find_element_by_xpath('//*[@id="content"]/div/header/div[2]/a/'
                                             'span').text == 'jinjie'.encode('utf-8'):
            print('yes')

        # 操作按钮
        nub_a = 1
        list_common_part = '//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/' \
                           'div/div/div/div/div/table/tbody/tr['
        list_type = ']/td[9]'
        list_operate = ']/td[10]/button'
        driver = self.driver
        try:
            driver.find_element_by_xpath(list_common_part + str(nub_a) + list_operate)
        except Exception as E:
            print(E)
        while nub_a <= 32:
            operate_button = list_common_part + str(nub_a) + list_operate
            type_button = list_common_part + str(nub_a) + list_type
            operate = driver.find_element_by_xpath(operate_button)
            types = driver.find_element_by_xpath(type_button)
            if operate.text == '操 作'.encode('utf-8'):
                if types.text == '已生成'.encode('utf-8'):
                    driver.find_element_by_xpath(operate_button).click()
                    time.sleep(3)
                    with open("../executor_url/current_url.txt", "r+") as current_url_file:
                        current_url_file.write(driver.current_url)
                        break
            nub_a = nub_a + 1
        else:
            x = 2
            part_one = '''//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/div/table/
                            tbody/tr['''
            part_two = ''']/td[10]/button'''
            while True:
                if driver.find_element_by_xpath(part_one + str(x) + part_two).text == '操作'.encode('utf-8'):
                    driver.find_element_by_xpath(part_one + str(x) + part_two).click()
                    with open("../executor_url/current_url.txt", "r+") as current_url_file:
                        current_url_file.write(driver.current_url)
                    time.sleep(3)
                    return
                x = x + 1
                if x > 34:
                    return
        common_part = '//*[@id="content"]/div/div/div[1]/div[1]/div[1]/section[2]/div'
        axial_pic = '//*[@id="content"]/div/div/div[1]/div[2]/div[1]/div/div[3]/div[1]/div/div/canvas'
        cpr_pic = '//*[@id="content"]/div/div/div[1]/div[2]/div[3]/div/div[3]'
        d3_pic = '//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div/div[1]/canvas'
        xsection_pic = '//*[@id="content"]/div/div/div[1]/div[2]/div[4]/div/div[2]/div[2]'
        lumen_pic = '//*[@id="content"]/div/div/div[1]/div[2]/div[5]/div/img'
        x = 1
        list_x = []
        while True:
            try:
                if driver.find_element_by_xpath(common_part + '[' + str(x) + ']'):
                    list_x.append(x)
                    x = x+1
                    continue
                else:
                    break
            except Exception as e:
                print(e)
                break
        try:
            for y in list_x:
                driver.find_element_by_xpath(common_part + '[' + str(y) + ']').click()
                # Axial图 放大，显示分割结果，滚动，隐藏，缩小
                axial_pic_obj = driver.find_element_by_xpath(axial_pic)
                webdriver.ActionChains(driver).double_click(axial_pic_obj).perform()
                time.sleep(5)
                driver.find_element_by_xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[1]/div/div[3]/div[2]'
                                             '/div[2]/button[1]').click()

                button = driver.find_element_by_css_selector('#content > div > div > div.coronary-image > '
                                                             'div.coronary-image--section.coronary-image--main > '
                                                             'div.coronary-image--left-part.active > div > '
                                                             'div.dicom-viewer-nav.full-pane > svg > polygon')
                action_axial = ActionChains(driver)
                action_axial.click_and_hold(button).perform()
                for x in range(5):
                    action_axial.move_by_offset(0, 2).perform()
                    focus = driver.find_element_by_xpath(
                        '//*[@id="content"]/div/div/div[1]/div[2]/div[1]/div/div[3]/div[1]'
                        '/div/div/div')
                    left_style = focus.value_of_css_property('left').encode('utf-8')
                    top_style = focus.value_of_css_property('top').encode('utf-8')
                    if data.left_style['left' + str(x + 1)] != left_style:
                        return
                    if data.top_style['top' + str(x + 1)] != top_style:
                        return
                    # 标注图像对比
                    time.sleep(1)
                action_axial.release().perform()
                big_axial_obj = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[1]/div/'
                                                             'div[3]/div[1]')
                webdriver.ActionChains(driver).double_click(big_axial_obj).perform()
                time.sleep(1)
                # cpr图操作
                cpr_pic_obj = driver.find_element_by_xpath(cpr_pic)
                webdriver.ActionChains(driver).double_click(cpr_pic_obj).perform()
                time.sleep(5)
                action_cpr = ActionChains(driver)
                for x in range(6):
                    action_cpr.key_down(Keys.DOWN).perform()
                    time.sleep(1)
                action_cpr.key_up(Keys.DOWN).perform()
                webdriver.ActionChains(driver).double_click(cpr_pic_obj).perform()
                time.sleep(1)

                # section图
                xsection_pic_obj = driver.find_element_by_xpath(xsection_pic)
                action_section = ActionChains(driver)
                action_section.move_to_element(xsection_pic_obj)
                action_section.click().perform()
                # 按下键向下滑
                nub = 1
                while nub < 20:
                    action_section.key_down(Keys.DOWN).perform()
                    time.sleep(1)
                    nub += nub
                action_section.key_up(Keys.DOWN).perform()

                # lumen图
                lumen_pic_obj = driver.find_element_by_xpath(lumen_pic)
                webdriver.ActionChains(driver).double_click(lumen_pic_obj).perform()
                action_lumen = ActionChains(driver)
                nub = 1
                while nub < 20:
                    action_lumen.key_down(Keys.DOWN).perform()
                    time.sleep(1)
                    nub += nub
                action_lumen.key_up(Keys.DOWN).perform()
                webdriver.ActionChains(driver).double_click(lumen_pic_obj).perform()

            # 3d 心肌图
            action_3d = ActionChains(driver)
            d3_pic_object = driver.find_element_by_xpath(d3_pic)
            webdriver.ActionChains(driver).double_click(d3_pic_object).perform()
            driver.find_element_by_xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div/div[2]/'
                                         'button').click()
            action_3d.click_and_hold(d3_pic_object).perform()
            for x in range(10):
                time.sleep(1)
                action_3d.move_by_offset(5, 1).perform()
                action_3d.release().perform()
            webdriver.ActionChains(driver).double_click(d3_pic_object).perform()
            print('stop')

        except NoSuchElementException as e:
            print(e)
            driver.get_screenshot_as_file(self.pic_path + str(time.strftime("%Y-%m-%d-%H_%M_%S",
                                                                            time.localtime(time.time()))) + '.png')
        except Exception as e:
            print(e)

        # 图片合格
        driver.find_element_by_xpath('//*[@id="content"]/div/div/div[1]/div[1]/div[2]/div/button[1]').click()
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div/div/button[1]').click()


if __name__ == '__main__':
    test = CTA()
    test.test_login()

