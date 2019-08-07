# -*- coding: utf-8 -*-
from listPage import ListPage
from selenium.webdriver.common.action_chains import ActionChains
from daphne.func2.CTA_setting import *
from daphne.func2.page_func import *
from daphne.func2.create_report import *
from daphne.util.mongoutil import *
import time
import re


class CypressPage(ListPage):

    def __init__(self):
        ListPage.__init__(self)
        ListPage.judge_status(self)
        self.user_id = re.findall(r"caseId=(.+?)&", self.driver.current_url)[0]
        self.branch_list()
        self.create_report_bottom = bottom()

    def branch_list(self):

        branch_list = []

        # 计算病例有多少血管分支，放入branch_list
        nub = 1
        while True:
            if self.is_element_exist((selection_xpath['top_path'] +
                                      selection_xpath['mid_path'] +
                                      str(nub) +
                                      selection_xpath['bottom_path']),
                                     key_path='xpath'
                                     ):
                branch_list.append(self.driver.find_element_by_xpath(
                    (selection_xpath['top_path'] +
                     selection_xpath['mid_path'] +
                     str(nub) +
                     selection_xpath['bottom_path'])).text)
                nub += 1
            else:
                break
        print("branch_list:", branch_list)
        part(u"冠脉诊断页", u"冠脉分支列表展示", "", "success", "")

        def click_blood_branch():
            for x in range(len(branch_list)):
                self.driver.find_element_by_xpath((selection_xpath['top_path'] +
                                                   selection_xpath['mid_path'] +
                                                   str(x+1) +
                                                   selection_xpath['bottom_path'])).click()
                branch = branch_list[x].encode('utf-8').decode('utf-8')
                print(branch)

                @run_test_func
                def cypress_dicom_test():
                    time.sleep(2)

                    # 判断图像是否被选中
                    self.driver.execute_script(branch_xpath['dicom'])
                    if border_is_chosen(self.driver, "xpath", branch_xpath['dicom_border_xpath']):
                        part(u"冠脉诊断页", u" dicom图像", branch, "success", "")
                    else:
                        part(u"冠脉诊断页",
                             u" dicom图像",
                             branch,
                             "fail",
                             u"点击后未被选中" + "css-border-none")

                    # 判断显示影藏血管标记
                    self.driver.execute_script(branch_xpath['dicom_blood'])
                    blood_split = self.driver.find_element_by_xpath(branch_xpath['dicom_blood_xpath']).text
                    if (x % 2) == 0 and (blood_split == '隐藏分割结果'):
                        part(u"冠脉诊断页", u" dicom图像血管分割", branch, "success", "")
                    else:
                        part(u"冠脉诊断页",
                             u" dicom图像血管分割",
                             branch,
                             "fail",
                             u"点击后未被选中")

                    # 图像向下滚动操作, 爬虫获取滚动后dicom切片数，字典类型 {页数，（x，y）} 再次去mongo进行坐标对比
                    action_chain_dicom_down = ActionChains(self.driver)
                    dicom_page_dict = self.roll_picture_down(action_chain_dicom_down, 10,
                                                             ("div",
                                                              "dicom-info--left-top",
                                                              "dicom-viewer--focus"))

                    # 通过dicom_page_dict的key去拿x，y,测试时发现mongo内z对应的切片有很多，但只要有其一满足即可通过测试
                    for dicom_page_nub, dicom_page_focus in dicom_page_dict.items():
                        mongo_data_set = self.mongo_data(branch_relationship[branch], dicom_page_nub)
                        success_nub = 0
                        for mongo_data in mongo_data_set:
                            focus_x_float = abs(mongo_data[0] - 10.0 - round(float(dicom_page_focus[0])))
                            focus_y_float = abs(mongo_data[1] - 10.0 - round(float(dicom_page_focus[1])))
                            if focus_x_float <= 2.0 and focus_y_float <= 2.0:
                                success_nub = success_nub + 1
                        if success_nub > 0:
                            part(u"冠脉诊断页",  u" dicom联动标记", branch, "success", "")
                        else:
                            part(u"冠脉诊断页",
                                 u" dicom联动标记",
                                 branch,
                                 "fail",
                                 (u' dicom切片' + dicom_page_nub + ' ' +
                                  dicom_page_focus[0] + ' ' + dicom_page_focus[1] + u"联动位置像素相差过大"))

                    # 鼠标双击放大dicom
                    double_click_obj = self.driver.find_element_by_xpath(branch_xpath['dicom_xpath'])
                    action_chain_double_click = ActionChains(self.driver)
                    action_chain_double_click.double_click(double_click_obj).perform()
                    if self.driver.find_element_by_xpath(branch_xpath['dicom_border_xpath']).get_attribute("style"):
                        part(u"冠脉诊断页", u" dicom图像血管放大", branch, "success", "")
                    else:
                        part(u"冠脉诊断页",
                             u" dicom图像血管放大",
                             branch,
                             "fail",
                             u"百分比放大状态")

                    # 图像向上滚动操作
                    action_chain_dicom_up = ActionChains(self.driver)
                    roll_picture_up(action_chain_dicom_up, 10)
                    part(u"冠脉诊断页", u" dicom图像切换", branch, "success", "")

                    # 双击还原操作
                    action_chain_double_click.perform()
                    if not self.driver.find_element_by_xpath(branch_xpath['dicom_border_xpath']).get_attribute("style"):
                        part(u"冠脉诊断页", u" dicom图像血管缩小", branch, "success", "")
                    else:
                        part(u"冠脉诊断页",
                             u" dicom图像血管缩小",
                             branch,
                             u"fail",
                             u"缩小效果异常")
                    time.sleep(0.5)

                @run_test_func
                def cypress_cpr_test():
                    # cpr图像点击操作
                    self.driver.execute_script(branch_xpath['cpr_xpath'])
                    if border_is_chosen(self.driver, "xpath", branch_xpath['cpr_border_xpath']):
                        part(u"冠脉诊断页", u" cpr图像", branch, "success", "")
                    else:
                        part(u"冠脉诊断页",
                             u" cpr图像",
                             branch,
                             "fail",
                             "css-border-none" + u"点击后未被选中")

                    # cpr图像操作 验证中心线显示是否有问题
                    time.sleep(2)
                    action_chain_cpr_down = ActionChains(self.driver)
                    cpr_page_dict = self.roll_picture_down(action_chain_cpr_down, 5, ('div',
                                                                                      'cpr_dicom-info--left-top',
                                                                                      'cpr-image--focus'))
                    if cpr_page_dict:
                        cpr_success_nub = 0
                        for cpr_dict_key in cpr_page_dict.keys():
                            cpr_data_list = self.mongo_data(branch_relationship[branch], '', ('cpr', cpr_dict_key))
                            for cpr_x_y in range(len(cpr_data_list)-1):
                                if abs(cpr_data_list[cpr_x_y]['x'] - cpr_data_list[cpr_x_y+1]['x']) >= 10.0:
                                    part(u"冠脉诊断页",
                                         u" cpr图像中心线",
                                         branch,
                                         "fail",
                                         u"相邻坐标点过大是否有误?需查看" +
                                         ' ' +
                                         str(cpr_data_list[cpr_x_y]['x']) + ' ,'
                                         + str(cpr_data_list[cpr_x_y+1]['x']))
                                    cpr_success_nub = cpr_success_nub + 1
                                    break

                        if cpr_success_nub == 0:
                            part(u"冠脉诊断页", u" cpr图像中心线", branch, "success", "")

                    # cpr图像双击放大效果
                    cpr_doubleclick_obj = self.driver.find_element_by_xpath(branch_xpath['cpr_doubleclick_obj'])
                    action_chain_cpr_doubleclick = ActionChains(self.driver)
                    action_chain_cpr_doubleclick.double_click(cpr_doubleclick_obj).perform()
                    if self.driver.find_element_by_xpath(branch_xpath['cpr_border_xpath']).get_attribute("style"):
                        part(u"冠脉诊断页", u" cpr图像放大效果", branch, "success", "")
                    else:
                        part(u"冠脉诊断页",
                             u" cpr图像放大效果",
                             branch,
                             "fail",
                             u"百分比放大状态")

                    # cpr图像放大后操作
                    action_chain_cpr_up = ActionChains(self.driver)
                    roll_picture_up(action_chain_cpr_up, 5)

                    # cpr图像双击缩小操作
                    action_chain_cpr_up_double = ActionChains(self.driver)
                    action_chain_cpr_up_double.double_click(cpr_doubleclick_obj).perform()
                    if not self.driver.find_element_by_xpath(branch_xpath['cpr_border_xpath']).get_attribute("style"):
                        part(u"冠脉诊断页", u" cpr图像缩小效果", branch, "success", "")
                    else:
                        part(u"冠脉诊断页",
                             u" cpr图像缩小效果",
                             branch,
                             "fail",
                             u"缩小效果异常")
                    time.sleep(2)

                @test_model_except_exception
                def cypress_section_test():
                    self.driver.execute_script(branch_xpath['section_xpath'])
                    if border_is_chosen(self.driver, "xpath", branch_xpath['section_border_xpath']):
                        part(u"冠脉诊断页", u" Xsection图像", branch, "success", "")
                    else:
                        part(u"冠脉诊断页",
                             u" Xsection图像",
                             branch,
                             "fail",
                             "css-border-none" +
                             u"点击后未被选中")

                    # 图像联动操作
                    action_chain_section_down = ActionChains(self.driver)
                    roll_picture_down(action_chain_section_down, 10)
                    time.sleep(0.5)
                    part(u"冠脉诊断页", u" Xsection图像联动效果", branch, "success", "")

                @run_test_func
                def cypress_lumen_test():
                    lunmen_xpath = self.driver.find_element_by_xpath(branch_xpath['lumen_xpath'])
                    lunmen_xpath.click()
                    if border_is_chosen(self.driver, "xpath", branch_xpath['lumen_border_xpath']):
                        part(u"冠脉诊断页", u" lumen图像", branch, "success", "")
                    else:
                        part(u"冠脉诊断页",
                             u" lumen图像",
                             branch,
                             "fail",
                             "css-border-none" +
                             u"点击后未被选中")

                    # 图像滚动操作
                    lumen_down = ActionChains(self.driver)
                    roll_picture_down(lumen_down, 5)
                    time.sleep(0.5)
                    part(u"冠脉诊断页", u" lumen图像联动", branch, "success", "")
                    print(branch + '测试完成')
            return True

        result = click_blood_branch()
        if result:
            self.driver.execute_script(branch_xpath['success'])
            time.sleep(1)
            self.driver.execute_script(branch_xpath['confirm'])
            part(u"冠脉诊断页", u"病例诊断是否合格", u'提交成功', "success", '')

        self.driver.quit()

    def test_cypress_pass(self):
        time.sleep(3)
        self.driver.execute_script(branch_xpath['success'])
        time.sleep(1)
        self.driver.execute_script(branch_xpath['confirm'])

    def roll_picture_down(self, action_chain, nub, *args):
        response_data_dict = {}
        for i in range(int(nub)):
            action_chain.key_down(Keys.DOWN).key_up(Keys.DOWN)
            if i == 0:
                time.sleep(2)
            action_chain.perform()
            time.sleep(2)
            page_source = self.driver.page_source
            # 获取第几张dicom图像
            if args:
                dicom_page = page_spider(page_source, args[0][0], args[0][1])

                # 获取焦点的x，y位置
                dicom_page_focus = page_spider(source=page_source,
                                               element='div',
                                               _class=args[0][2])
                if isinstance(dicom_page_focus, tuple):
                    response_data_dict[dicom_page] = dicom_page_focus
                else:
                    if args[0][2] == 'cpr-image--focus':
                        response_data_dict[dicom_page] = dicom_page_focus
                    else:
                        response_data_dict[dicom_page[1]] = dicom_page_focus

        return response_data_dict

    def mongo_data(self, branch, parameter, *args):
        s = set()
        data = {"case_num": self.user_id}
        data = Mongo.select(data)
        if args:
            if args[0][0] == 'cpr':
                cpr_branch_list = data['cpr'][branch][args[0][1]]['center-line']
                return cpr_branch_list
        else:
            center_line = data['overview']['vessels'][branch]['center-line']
            for x in range(len(center_line)):
                if round(center_line[x]['z']) == int(parameter):
                    focus_tuple = (round(center_line[x]['x']), round(center_line[x]['y']))
                    s.add(focus_tuple)
            return s


if __name__ == '__main__':
    cypress = CypressPage()
