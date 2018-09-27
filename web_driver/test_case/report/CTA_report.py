# -*- coding: utf-8 -*-

import time
import sys
import shutil
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from PIL import Image
from PIL import ImageChops
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class CtaReport(object):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # patientId = u'程淑芬'
    _url = 'http://103.211.47.130:74/?type=all'
    _driver = '../../chrome_driver/chromedriver'
    _chrome_options = Options()
    _chrome_options.add_argument('--headless')
    _chrome_options.add_argument('--disable-gpu')
    _chrome_options.add_argument('--no-sandbox')
    _errorList = []
    picpath = '../dicom_picture/'
    cut_picpath = '../cut_picture/'
    original_pic_path = '../original_picture/'
    differ = '../differ/'

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
        # 清空differ, cut_picture, dicom_picture 内文件
        shutil.rmtree('../cut_picture')
        shutil.rmtree('../dicom_picture')
        shutil.rmtree('../differ')
        os.mkdir('../cut_picture')
        os.mkdir('../dicom_picture')
        os.mkdir('../differ')

    def operate_in(self):
        search_xpath = '//*[@id="content"]/div/div/header/div[3]/span/input'
        self.driver.find_element_by_xpath(search_xpath).send_keys(u"程淑芬")
        operate_button = '//*[@id="content"]/div/div/div/div/div[1]/div/div/div/div/table/tbody/tr[1]/td[13]/button'
        self.driver.find_element_by_xpath(operate_button).click()
        time.sleep(5)

    def dicom_test(self):
        # 操作
        time.sleep(5)
        dr = self.driver
        dr.find_element_by_xpath('//*[@id="content"]/div/div/section/div/div[2]/div[1]/div').click()
        time.sleep(1)
        js = "document.getElementsByClassName('ant-btn btn-show')[0].click()"
        dr.execute_script(js)
        # 截图
        dr.get_screenshot_as_file(CtaReport.picpath + 'dicom_1.png')

        # 滚动后截图
        action_axial = ActionChains(dr)
        for i in range(10):
            action_axial.key_down(Keys.DOWN)
            action_axial.key_up(Keys.DOWN)
            if i == 0:
                time.sleep(2)
            action_axial.perform()
            time.sleep(3)
            dr.get_screenshot_as_file(CtaReport.picpath + 'dicom_' + str(i+2) + '.png')
        print("dicom 鼠标中轴滚动操作完成")

        # 对比图像
        for y in range(11):
            nub = str(y+1)
            if not self.cut_picture(image=(CtaReport.picpath + 'dicom_' + nub + '.png'), status="dicom",
                                    spath=(CtaReport.cut_picpath + 'dicom_cut_' + nub + '.png')):
                return u"dicom调用剪切函数失败"
                # 原始值对比
            self.compare_picture(path_one=(CtaReport.original_pic_path + 'dicom_cut_' + nub + '.png'),
                                 path_two=(CtaReport.cut_picpath + 'dicom_cut_' + nub + '.png'),
                                 diff_save_location=(CtaReport.differ + 'differ_dicom_' + nub + '.png'))

    def cpr_test(self):
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div/section/div/div[2]/div[3]/div').click()
        time.sleep(2)
        dr = self.driver
        dr.execute_script("document.getElementsByClassName('ant-btn btn-show')[4].click()")
        action_axial = ActionChains(dr)
        for i in range(10):
            action_axial.key_down(Keys.DOWN)
            action_axial.key_up(Keys.DOWN)
            if i == 0:
                time.sleep(2)
            action_axial.perform()
            time.sleep(3)
            dr.get_screenshot_as_file(CtaReport.picpath + 'cpr_' + str(i+1) + '.png')
        print("cpr 鼠标中轴滚动操作完成")

        # 剪切对比图像
        for y in range(10):
            nub = str(y + 1)
            if not self.cut_picture(image=(CtaReport.picpath + 'cpr_' + nub + '.png'), status="dicom",
                                    spath=(CtaReport.cut_picpath + 'cpr_cut_' + nub + '.png')):
                return u"dicom调用剪切函数失败"
            # 原始值对比
            self.compare_picture(path_one=(CtaReport.original_pic_path + 'cpr_cut_' + nub + '.png'),
                                 path_two=(CtaReport.cut_picpath + 'cpr_cut_' + nub + '.png'),
                                 diff_save_location=(CtaReport.differ + 'differ_cpr_' + nub + '.png'))

    def lumen_test(self):
        time.sleep(2)
        dr = self.driver
        dr.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='WL:'])[3]/following::div[18]").click()
        dr.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='LAD远段'])[2]/following::button[1]").click()
        # 拉直

    def compare_report(self):
        x = 2
        branchlist = []
        while True:
            try:
                compart = '//*[@id="content"]/div/div/section/aside/div/div[1]/div[' + str(x) + ']/div/div[1]'
                branchlist.append(self.driver.find_element_by_xpath(compart).text.encode('utf-8'))
                x = x+1
                if x > 18:
                    break
            except NoSuchElementException:
                break
            except Exception as e:
                print(e)
                return

        border = '//*[@id="content"]/div/div/section/aside/div/div[1]/div['
        report_button = '//*[@id="content"]/div/div/section/aside/div/div[2]/div'
        report_close_button = '/html/body/div[3]/div/div[2]/div/div[1]/button/span'

        for index, branch in enumerate(branchlist):
            plaque_lm = border + str(index + 2) + ']/div/div[2]/div[1]/div/div'
            plaque = border + str(index + 2) + ']/div/div[2]/div[1]'
            plaque_1 = border + str(index + 2) + ']/div/div[2]/div[1]/div/ul/li[1]/label/span[1]/input'
            plaque_2 = border + str(index + 2) + ']/div/div[2]/div[1]/div/ul/li[2]/label/span[1]/input'
            plaque_3 = border + str(index + 2) + ']/div/div[2]/div[1]/div/ul//li[3]/label/span[1]/input'
            narrow = border + str(index + 2) + ']/div/div[2]/div[2]/div/div/div'
            narrow_list = border + str(index + 2)
            narrow_list_0 = narrow_list + ']/div/div[2]/div[2]/div/div/ul/li[1]'
            narrow_list_2 = narrow_list + ']/div/div[2]/div[2]/div/div/ul/li[2]'
            narrow_list_3 = narrow_list + ']/div/div[2]/div[2]/div/div/ul/li[3]'
            narrow_list_4 = narrow_list + ']/div/div[2]/div[2]/div/div/ul/li[4]'
            narrow_list_5 = narrow_list + ']/div/div[2]/div[2]/div/div/ul/li[5]'

            if branch == 'LM':
                self.driver.find_element_by_xpath(border + str(index + 2)+']').click()

                # 调用初始方法
                if not self.init_plaque_narrow(plaque_lm, plaque_1, plaque_2, plaque_3, narrow, narrow_list_0):
                    return "LM init error"

                # 开始lm的交叉组合测试报告
                # case_1 LM 钙化，轻度狭窄
                self.driver.find_element_by_xpath(plaque_lm).click()
                self.driver.find_element_by_xpath(plaque_1).click()
                self.driver.find_element_by_xpath(plaque_lm).click()
                self.driver.find_element_by_xpath(narrow).click()
                self.driver.find_element_by_xpath(narrow_list_3).click()
                time.sleep(1)
                self.driver.find_element_by_xpath(report_button).click()
                time.sleep(1)

                if self.driver.find_element_by_xpath('//*[@id="report"]/span[9]').text != '左主干（LM）显影好，管壁钙' \
                                                                                          '化斑块，管腔狭窄25-49%':
                    error = "LM case1 fail"
                    print(error)
                    CtaReport._errorList.append(error)
                    time.sleep(1)
                self.driver.find_element_by_xpath(report_close_button).click()
                # case2 无钙化无狭窄
                self.init_plaque_narrow(plaque_lm, plaque_1, plaque_2, plaque_3, narrow, narrow_list_0)
                time.sleep(1)
                self.driver.find_element_by_xpath(report_button).click()

                if self.driver.find_element_by_xpath('//*[@id="report"]/span[9]').text != '左主干（' \
                                                                                          'LM）显影好，未见斑块及狭窄':
                    error = "LM case2 fail"
                    CtaReport._errorList.append(error)
                time.sleep(1)
                self.driver.find_element_by_xpath(report_close_button).click()

            if branch == 'LAD近段':
                self.driver.find_element_by_xpath(border + str(index + 2) + ']').click()
                if not self.init_plaque_narrow(plaque, plaque_1, plaque_2, plaque_3, narrow, narrow_list_0):
                    return "LAD init error"
                # lad中段
                lad_mid_plaque_narrow_dict = self.create_plaque_narrow(border, index + 2 + 1)
                # lad远段
                lad_distal_plaque_narrow_dict = self.create_plaque_narrow(border, index + 2 + 2)
                self.driver.find_element_by_xpath(border + str(index + 2 + 1) + ']').click()
                # lad中段初始化
                if not self.init_plaque_narrow(lad_mid_plaque_narrow_dict['plaque'],
                                               lad_mid_plaque_narrow_dict['plaque_1'],
                                               lad_mid_plaque_narrow_dict['plaque_2'],
                                               lad_mid_plaque_narrow_dict['plaque_3'],
                                               lad_mid_plaque_narrow_dict['narrow'],
                                               lad_mid_plaque_narrow_dict['narrow_list_0']):
                    return "LAD mid init error"

                self.driver.find_element_by_xpath(border + str(index + 2 + 2) + ']').click()
                # lad远段初始化
                if not self.init_plaque_narrow(lad_distal_plaque_narrow_dict['plaque'],
                                               lad_distal_plaque_narrow_dict['plaque_1'],
                                               lad_distal_plaque_narrow_dict['plaque_2'],
                                               lad_distal_plaque_narrow_dict['plaque_3'],
                                               lad_distal_plaque_narrow_dict['narrow'],
                                               lad_distal_plaque_narrow_dict['narrow_list_0']):
                    return "LAD mid init error"
                time.sleep(1)
                self.driver.find_element_by_xpath(report_button).click()
                time.sleep(1)

                # case1 lad 无钙化无狭窄
                if self.driver.find_element_by_xpath('//*[@id="report"]/span[11]').text != '左前降支（LAD）未见斑块及狭窄' \
                        and ('LM' in branchlist):
                    error = "lad case1 fail"
                    CtaReport._errorList.append(error)
                self.driver.find_element_by_xpath(report_close_button).click()

                # case2 lad 近中远 钙化，轻度狭窄
                self.driver.find_element_by_xpath(border + str(index + 2) + ']').click()
                self.change_click_border(plaque, plaque_1, narrow, narrow_list_3, report_button='')
                self.driver.find_element_by_xpath(border + str(index + 2 + 1) + ']').click()
                self.change_click_border(lad_mid_plaque_narrow_dict['plaque'],
                                         lad_mid_plaque_narrow_dict['plaque_1'],
                                         lad_mid_plaque_narrow_dict['narrow'],
                                         lad_mid_plaque_narrow_dict['narrow_list_3'],
                                         report_button='')
                self.driver.find_element_by_xpath(border + str(index + 2 + 2) + ']').click()
                self.change_click_border(lad_distal_plaque_narrow_dict['plaque'],
                                         lad_distal_plaque_narrow_dict['plaque_1'],
                                         lad_distal_plaque_narrow_dict['narrow'],
                                         lad_distal_plaque_narrow_dict['narrow_list_3'],
                                         report_button=report_button)
                lm_span_11 = self.driver.find_element_by_xpath('//*[@id="report"]/span[11]')
                if lm_span_11.text != '左前降支（LAD）管壁钙化斑块，管腔狭窄25-49%' \
                        and ('LM' in branchlist):
                    error = "lad case2 fail"
                    CtaReport._errorList.append(error)
                self.driver.find_element_by_xpath(report_close_button).click()

                # --case3 近段无，中段钙化，中度狭窄  远段，非钙化，重度狭窄
                # 先初始近段，中段， 远段
                if not self.init_lad(border,
                                     index,
                                     plaque,
                                     plaque_1,
                                     plaque_2,
                                     plaque_3,
                                     narrow,
                                     narrow_list_0):
                    error = "lad case3 init fail"
                    CtaReport._errorList.append(error)
                    break
                # 中段
                self.driver.find_element_by_xpath(border + str(index + 2 + 1) + ']').click()
                self.change_click_border(lad_mid_plaque_narrow_dict['plaque'],
                                         lad_mid_plaque_narrow_dict['plaque_1'],
                                         lad_mid_plaque_narrow_dict['narrow'],
                                         lad_mid_plaque_narrow_dict['narrow_list_4'],
                                         report_button='')
                # 远段
                self.driver.find_element_by_xpath(border + str(index + 2 + 2) + ']').click()
                self.change_click_border(lad_distal_plaque_narrow_dict['plaque'],
                                         lad_distal_plaque_narrow_dict['plaque_3'],
                                         lad_distal_plaque_narrow_dict['narrow'],
                                         lad_distal_plaque_narrow_dict['narrow_list_5'],
                                         report_button=report_button)
                lad_span_11 = self.driver.find_element_by_xpath('//*[@id="report"]/span[11]')
                lad_span_13 = self.driver.find_element_by_xpath('//*[@id="report"]/span[13]')
                lad_span_15 = self.driver.find_element_by_xpath('//*[@id="report"]/span[15]')

                if (
                    lad_span_11.text != '左前降支近段（pLAD）未见斑块及狭窄'
                    and lad_span_13.text != '中段（mLAD）管壁钙化斑块，管腔狭窄50-69%'
                    and lad_span_15.text != '远段（dLAD）管壁非钙化斑块，管腔狭窄70-99%'
                    and ('LM' in branchlist)
                ):
                    error = "lad case3 fail"
                    CtaReport._errorList.append(error)
                self.driver.find_element_by_xpath(report_close_button).click()
                # case4 --近中段 混合 中度狭窄 远段 钙化，轻度
                if not self.init_lad(border,
                                     index,
                                     plaque,
                                     plaque_1,
                                     plaque_2,
                                     plaque_3,
                                     narrow,
                                     narrow_list_0):
                    error = "lad case3 init fail"
                    CtaReport._errorList.append(error)
                    return "ad case3 init fail"
                # 近段
                self.driver.find_element_by_xpath(border + str(index + 2) + ']').click()
                self.change_click_border(plaque,
                                         plaque_3,
                                         narrow,
                                         narrow_list_4,
                                         report_button='')
                # 中段
                self.driver.find_element_by_xpath(border + str(index + 2 + 1) + ']').click()
                self.change_click_border(lad_mid_plaque_narrow_dict['plaque'],
                                         lad_mid_plaque_narrow_dict['plaque_4'],
                                         lad_mid_plaque_narrow_dict['narrow'],
                                         lad_mid_plaque_narrow_dict['narrow_list_5'],
                                         report_button='')
                # 远段
                self.driver.find_element_by_xpath(border + str(index + 2 + 2) + ']').click()
                self.change_click_border(lad_distal_plaque_narrow_dict['plaque'],
                                         lad_distal_plaque_narrow_dict['plaque_1'],
                                         lad_distal_plaque_narrow_dict['narrow'],
                                         lad_distal_plaque_narrow_dict['narrow_list_3'],
                                         report_button=report_button)
                span_11 = self.driver.find_element_by_xpath('//*[@id="report"]/span[11]')
                span_13 = self.driver.find_element_by_xpath('//*[@id="report"]/span[13]')

                if (
                    span_11.text != '左前降支近段（pLAD）、中段（mLAD）管壁混合斑块，管腔狭窄50-69%'
                    and span_13.text != '远段（dLAD）管壁钙化斑块，管腔狭窄25-49%'
                    and ('LM' in branchlist)
                ):
                    error = "lad case4 fail"
                    CtaReport._errorList.append(error)
                self.driver.find_element_by_xpath(report_close_button).click()
                self.init_lad(border,
                              index,
                              plaque,
                              plaque_1,
                              plaque_2,
                              plaque_3,
                              narrow,
                              narrow_list_0)

            if branch == 'D1':
                self.driver.find_element_by_xpath(border + str(index + 2) + ']').click()
                if not self.init_plaque_narrow(plaque,
                                               plaque_1,
                                               plaque_2,
                                               plaque_3,
                                               narrow,
                                               narrow_list_0):
                    return "D1 init error"

                if branchlist[index + 1] == 'D2':
                    dict_d2 = self.create_plaque_narrow(border, index + 1)
                    self.driver.find_element_by_xpath(border + str(index + 2 + 1) + ']').click()
                    if not self.init_plaque_narrow(dict_d2['plaque'],
                                                   dict_d2['plaque_1'],
                                                   dict_d2['plaque_2'],
                                                   dict_d2['plaque_3'],
                                                   dict_d2['narrow'],
                                                   dict_d2['narrow_list_0']):
                        return "D2 init error"
                    # --case 1 D1 D2 钙化 轻微狭窄
                    self.driver.find_element_by_xpath(border + str(index + 2) + ']').click()
                    self.change_click_border(plaque,
                                             plaque_1,
                                             narrow,
                                             narrow_list_2,
                                             report_button='')
                    self.driver.find_element_by_xpath(border + str(index + 2 + 1) + ']').click()
                    self.change_click_border(dict_d2['plaque'],
                                             dict_d2['plaque_1'],
                                             dict_d2['narrow'],
                                             dict_d2['narrow_list_2'],
                                             report_button=report_button)
                    span_15 = self.driver.find_element_by_xpath('//*[@id="report"]/span[15]')
                    if span_15.text != '对角支（D1、D2）管壁钙化斑块，管腔狭窄1-24%':
                        error = "D1 D2 case1 fail"
                        CtaReport._errorList.append(error)
                    self.driver.find_element_by_xpath(report_close_button).click()

                    # --case2 D1 钙化 轻微狭窄 D2 非钙化 轻度

        print("done")
        print(CtaReport._errorList)

    def post_report(self):
        # 推送
        pass

    def print_report(self):
        # 打印
        pass

    def finally_done(self):
        self.driver.quit()

    def is_checked(self, css_data):
        js = "document.getElementsByClassName('" + css_data + "')"
        try:
            if self.driver.execute_script(js):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def init_plaque_narrow(self, plaque, plaque_1, plaque_2, plaque_3, narrow, narrow_list_0):
        try:
            self.driver.find_element_by_xpath(plaque).click()
            lm_plaque_choose_1 = self.driver.find_element_by_xpath(plaque_1)
            lm_plaque_choose_2 = self.driver.find_element_by_xpath(plaque_2)
            lm_plaque_choose_3 = self.driver.find_element_by_xpath(plaque_3)
            # 还原为原始状态，都为未选择
            if lm_plaque_choose_1.is_selected():
                lm_plaque_choose_1.click()
            if lm_plaque_choose_2.is_selected():
                lm_plaque_choose_2.click()
            if lm_plaque_choose_3.is_selected():
                lm_plaque_choose_3.click()
            self.driver.find_element_by_xpath(plaque).click()
            time.sleep(1)
            # 狭窄操作
            self.driver.find_element_by_xpath(narrow).click()
            lm_narrow_choose = self.driver.find_element_by_xpath(narrow_list_0)
            lm_narrow_choose.click()
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def change_click_border(self, plaque, plaque_x, narrow, narrow_list_x, report_button):
        self.driver.find_element_by_xpath(plaque).click()
        self.driver.find_element_by_xpath(plaque_x).click()
        self.driver.find_element_by_xpath(plaque).click()
        self.driver.find_element_by_xpath(narrow).click()
        self.driver.find_element_by_xpath(narrow_list_x).click()
        time.sleep(1)
        if report_button != '':
            self.driver.find_element_by_xpath(report_button).click()
            time.sleep(1)
        return True

    def init_lad(self, border, index, plaque, plaque_1,  plaque_2, plaque_3, narrow, narrow_list_0):
        self.driver.find_element_by_xpath(border + str(index + 2) + ']').click()
        if not self.init_plaque_narrow(plaque, plaque_1, plaque_2, plaque_3, narrow, narrow_list_0):
            return "LAD init error"

        # lad中段
        lad_mid_plaque_narrow_dict = self.create_plaque_narrow(border, index + 2 + 1)

        # lad远段
        lad_distal_plaque_narrow_dict = self.create_plaque_narrow(border, index + 2 + 2)

        self.driver.find_element_by_xpath(border + str(index + 2 + 1) + ']').click()

        # lad中段初始化
        if not self.init_plaque_narrow(lad_mid_plaque_narrow_dict['plaque'],
                                       lad_mid_plaque_narrow_dict['plaque_1'],
                                       lad_mid_plaque_narrow_dict['plaque_2'],
                                       lad_mid_plaque_narrow_dict['plaque_3'],
                                       lad_mid_plaque_narrow_dict['narrow'],
                                       lad_mid_plaque_narrow_dict['narrow_list_0']):
            return "LAD mid init error"

        self.driver.find_element_by_xpath(border + str(index + 2 + 2) + ']').click()

        # lad远段初始化
        if not self.init_plaque_narrow(lad_distal_plaque_narrow_dict['plaque'],
                                       lad_distal_plaque_narrow_dict['plaque_1'],
                                       lad_distal_plaque_narrow_dict['plaque_2'],
                                       lad_distal_plaque_narrow_dict['plaque_3'],
                                       lad_distal_plaque_narrow_dict['narrow'],
                                       lad_distal_plaque_narrow_dict['narrow_list_0']):
            return "LAD mid init error"
        return True

    @staticmethod
    def create_plaque_narrow(border, index):
        plaque_narrow_dict = dict()
        plaque_narrow_dict['plaque'] = border + str(index) + ']/div/div[2]/div[1]'
        plaque_narrow_dict['plaque_1'] = border + str(index) + ']/div/div[2]/div[1]/div/ul/li[1]/label/span[1]/input'
        plaque_narrow_dict['plaque_2'] = border + str(index) + ']/div/div[2]/div[1]/div/ul/li[2]/label/span[1]/input'
        plaque_narrow_dict['plaque_3'] = border + str(index) + ']/div/div[2]/div[1]/div/ul//li[3]/label/span[1]/input'
        plaque_narrow_dict['narrow'] = border + str(index) + ']/div/div[2]/div[2]/div/div/div'
        narrow_list = border + str(index)
        plaque_narrow_dict['narrow_list'] = narrow_list
        plaque_narrow_dict['narrow_list_0'] = narrow_list + ']/div/div[2]/div[2]/div/div/ul/li[1]'
        plaque_narrow_dict['narrow_list_2'] = narrow_list + ']/div/div[2]/div[2]/div/div/ul/li[2]'
        plaque_narrow_dict['narrow_list_3'] = narrow_list + ']/div/div[2]/div[2]/div/div/ul/li[3]'
        plaque_narrow_dict['narrow_list_4'] = narrow_list + ']/div/div[2]/div[2]/div/div/ul/li[4]'
        plaque_narrow_dict['narrow_list_5'] = narrow_list + ']/div/div[2]/div[2]/div/div/ul/li[5]'
        return plaque_narrow_dict

    @staticmethod
    def cut_picture(image, status, spath):
        im = Image.open(image)
        print("图像的宽度与高度是{}".format(im.size))
        if status == 'dicom':
            region = im.crop((600, 330, 1350, 650))
            region.save(spath)
            return True

    @staticmethod
    def compare_picture(path_one, path_two, diff_save_location):
        image_one = Image.open(path_one)
        image_two = Image.open(path_two)
        try:
            diff = ImageChops.difference(image_one, image_two)
            if diff.getbbox() is None:
                print("【+】We are the same!")
            else:
                diff.save(diff_save_location)
        except ValueError as e:
            print("{0}".format(e))

    @staticmethod
    def runner():
        CtaReport.operate_in()
        # CtaReport.dicom_test()
        CtaReport.lumen_test()
        # CtaReport.compare_report()
        CtaReport.finally_done()


if __name__ == '__main__':
    CtaReport = CtaReport()
    CtaReport.runner()
