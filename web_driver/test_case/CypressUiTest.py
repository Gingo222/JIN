# -*- coding: utf-8 -*-

import unittest
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# patientId = u'程淑芬'

reload(sys)
sys.setdefaultencoding('utf-8')


class ReuseChrome(Remote):

    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        """
        重写start_session方法
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})
        self.capabilities = options.Options().to_capabilities()
        self.session_id = self.r_session_id
        self.w3c = False


class JobTest(unittest.TestCase):
    _sessionId_file = '../sessionId/sessionId.txt'
    _executor_url_file = '../executor_url/executor_url.txt'
    _current_url_file = '../executor_url/current_url.txt'
    _cdriver = "../chrome_driver/chromedriver"
    _chrome_options = Options()
    # _chrome_options.add_argument('--headless')
    # _chrome_options.add_argument('--disable-gpu')
    # _chrome_options.add_argument('--no-sandbox')
    os.environ["webdriver.chrome.driver"] = _cdriver

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=JobTest._cdriver, chrome_options=JobTest._chrome_options)
        self.url = 'http://103.211.47.130:70/'
        self.pic_path = 'picture/'
        self.driver.implicitly_wait(30)
        self.sessionId = self.driver.session_id
        self.executor_url = self.driver.command_executor._url

    def test_Login(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        # 登录
        self.driver.find_element_by_xpath('//*[@id="userName"]').send_keys('jinjie')
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div/main/div/div/div/div[2]/form/div[3]'
                                          '/div/div/span/button').click()
        print(self.sessionId)
        name = '//*[@id="content"]/div/header/div[2]/a/span'
        locator = (By.XPATH, name)
        WebDriverWait(self.driver, 10, 3).until(EC.presence_of_element_located(locator))
        if self.driver.find_element_by_xpath(name).text == 'jinjie'.encode('utf-8'):
            self.assertEqual("login_Pass", "login_Pass")
            with open(JobTest._sessionId_file, "r+")as SessionFile:
                SessionFile.write(self.sessionId)
            with open(JobTest._executor_url_file, "r+") as executor_url_file:
                executor_url_file.write(self.executor_url)
                return
        else:
            self.assertEqual("error", "login fail")
            return

    def test_Operate(self):
        self.driver.quit()
        del self.driver
        session_file = open(JobTest._sessionId_file)
        session_id = session_file.read()
        session_file.close()
        executor_url_file = open(JobTest._executor_url_file)
        executor_url = executor_url_file.read()
        executor_url_file.close()
        driver = ReuseChrome(command_executor=executor_url, session_id=session_id)
        driver.get(self.url)
        # 操作按钮
        nub_a = 1
        list_common_part = '//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/' \
                           'div/div/div/div/div/table/tbody/tr['
        list_type = ']/td[9]'
        list_operate = ']/td[10]/button'
        try:
            driver.find_element_by_xpath(list_common_part + str(nub_a) + list_operate)
        except Exception as E:
            print(E)
            self.assertEqual("error", "no data for show")
            return
        while nub_a <= 32:
            operate_button = list_common_part + str(nub_a) + list_operate
            type_button = list_common_part + str(nub_a) + list_type
            operate = driver.find_element_by_xpath(operate_button)
            types = driver.find_element_by_xpath(type_button)
            if operate.text == '操 作'.encode('utf-8'):
                if types.text == '已生成'.encode('utf-8'):
                    driver.find_element_by_xpath(operate_button).click()
                    time.sleep(3)
                    with open(JobTest._current_url_file, "r+") as current_url_file:
                        current_url_file.write(driver.current_url)
                        self.assertEqual("operate_success", "operate_success")
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
                    self.assertEqual("operate_pass", "operate_pass")
                    with open(JobTest._current_url_file, "r+") as current_url_file:
                        current_url_file.write(driver.current_url)
                    time.sleep(3)
                    return
                x = x + 1
                if x > 34:
                    self.assertEqual("error", "no operate for click")
                    return

    def test_Coronary_Info(self):
        self.driver.quit()
        del self.driver
        session_file = open(JobTest._sessionId_file)
        session_id = session_file.read()
        session_file.close()
        executor_url_file = open(JobTest._executor_url_file)
        executor_url = executor_url_file.read()
        executor_url_file.close()
        driver = ReuseChrome(command_executor=executor_url, session_id=session_id)
        current_url_file = open(JobTest._current_url_file)
        driver.get(str(current_url_file.read()))
        current_url_file.close()
        time.sleep(5)
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

                # Axial图 放大，显示分割结果，滚动，隐藏，缩小，验证坐标点，验证标注
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
                for x in range(10):
                    action_axial.move_by_offset(0, 2).perform()
                    # 验证标注
                    focus = driver.find_element_by_xpath(
                        '//*[@id="content"]/div/div/div[1]/div[2]/div[1]/div/div[3]/div[1]'
                        '/div/div/div')
                    left_style = focus.value_of_css_property('left').encode('utf-8')
                    top_style = focus.value_of_css_property('top').encode('utf-8')
                    '''
                    # 需要测试数数据得到准确的坐标json
                    if data.left_style['left' + str(x + 1)] != left_style:
                        self.assertEqual("error", "left_style != data.left_style ")
                    if data.top_style['top' + str(x + 1)] != top_style:
                        self.assertEqual("error", "top_style != data.top_style")
                    '''
                    time.sleep(1)
                action_axial.release().perform()
                big_axial_obj = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[1]/div/'
                                                             'div[3]/div[1]')
                time.sleep(1)
                webdriver.ActionChains(driver).double_click(big_axial_obj).perform()
                time.sleep(1)

                # cpr图操作
                cpr_pic_obj = driver.find_element_by_xpath(cpr_pic)
                webdriver.ActionChains(driver).double_click(cpr_pic_obj).perform()
                time.sleep(5)
                action_cpr = ActionChains(driver)
                for x in range(5):
                    action_cpr.key_down(Keys.DOWN).key_up(Keys.DOWN).perform()
                    time.sleep(1)
                # action_cpr.key_up(Keys.DOWN).perform()
                webdriver.ActionChains(driver).double_click(cpr_pic_obj).perform()
                time.sleep(1)

                # section图，联动效果验证
                xsection_pic_obj = driver.find_element_by_xpath(xsection_pic)
                action_section = ActionChains(driver)
                action_section.move_to_element(xsection_pic_obj)
                action_section.click().perform()
                # 按下键向下滑
                nub = 1
                while nub < 20:
                    action_section.key_down(Keys.DOWN).key_up(Keys.DOWN).perform()
                    # 对比联动效果
                    time.sleep(1)
                    nub += nub
                # action_section.key_up(Keys.DOWN).perform()

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
                time.sleep(3)

            # 3d心肌图
            action_3d = ActionChains(driver)
            d3_pic_object = driver.find_element_by_xpath(d3_pic)
            webdriver.ActionChains(driver).double_click(d3_pic_object).perform()
            driver.find_element_by_xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div/div[2]/'
                                         'button').click()
            action_3d.click_and_hold(d3_pic_object).perform()
            for x in range(10):
                time.sleep(0.5)
                action_3d.move_by_offset(8, 3).perform()
                action_3d.release().perform()
            webdriver.ActionChains(driver).double_click(d3_pic_object).perform()
            self.assertEqual("test_Coronary_Info pass", "test_Coronary_Info pass")

        except NoSuchElementException as e:
            print(e)
            driver.get_screenshot_as_file(self.pic_path + str(time.strftime("%Y-%m-%d-%H_%M_%S",
                                                                            time.localtime(time.time()))) + '.png')
            self.assertEqual("error", "NoSuchElementException")
        except Exception as e:
            self.assertEqual("error", str(e))

    @staticmethod
    def del_file_info():
        with open(JobTest._sessionId_file, 'r+')as s:
            s.write('')
        with open(JobTest._current_url_file, 'r+')as c:
            c.write('')
        with open(JobTest._executor_url_file, 'r+')as e:
            e.write('')

    def quitBrowser(self):
        del self.driver
        self.driver.quit()
