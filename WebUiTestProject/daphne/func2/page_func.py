# -*- coding: utf-8 -*-
import time
import re
import sys
from cta_error import CtaTestCaseError
from selenium.webdriver.common.keys import *
from bs4 import BeautifulSoup


error_list = []
reload(sys)
sys.setdefaultencoding('utf-8')


def test_model_except_exception(func):
    def except_exception():
        try:
            func()
        except Exception as e:
            error_list.append(func.__name__)
            print(e)
            # 加入html
            raise CtaTestCaseError(errorInfo=func.__name__)
        else:
            return True
    return except_exception()


def roll_picture_down(action_chain, nub, *args):
    for i in range(int(nub)):
        action_chain.key_down(Keys.DOWN).key_up(Keys.DOWN)
        if i == 0:
            time.sleep(2)
        action_chain.perform()
        time.sleep(2)
        # 获取第几张dicom图像
        if args:
            page_spider(args[0][0], args[0][1], args[0][2])


def roll_picture_up(action_chain, nub):
    for i in range(int(nub)):
        action_chain.key_down(Keys.UP).key_up(Keys.UP)
        if i == 0:
            time.sleep(2)
        action_chain.perform()
        time.sleep(2)


def run_test_func(func):
    def run():
        func()
    return run()


def border_is_chosen(driver, state, value):
    if not state:
        return False
    if state == 'classname':
        link = driver.find_element_by_class_name(value)
        if link.value_of_css_property("border"):
            return True
        return False
    elif state == 'xpath':
        link = driver.find_element_by_xpath(value)
        if link.value_of_css_property("border"):
            return True
        return False


def page_spider(source, element, _class):
    soup = BeautifulSoup(source, 'html.parser')
    if _class == 'dicom-info--left-top':
        div = soup.find_all(element, _class)
        data = re.findall(r"Axial(.+?)/", div[0].encode('utf-8'))
        need_data = data[0].lstrip(' ')
        return need_data

    elif _class == 'dicom-viewer--focus':
        div = soup.find_all(element, _class)
        left_data = re.findall(r"left:(.+?)px", div[0].encode('utf-8'))
        top_data = re.findall(r"top:(.+?)px", div[0].encode('utf-8'))
        if left_data and top_data:
            res = (left_data[0].strip(' '), top_data[0].strip(' '))
            return res
        return False

    elif _class == 'cpr_dicom-info--left-top':
        div = soup.find_all(element, 'dicom-info--left-top')
        for x in div:
            if re.findall(r"Angle: (.+?)/", x.encode('utf-8')):
                data = re.findall(r"Angle: (.+?)/", x.encode('utf-8'))
                data = data[0].strip(' ')
                data = data.replace(' ', '').replace('<br', '')
                return data
        return False

    elif _class == 'cpr-image--focus':
        div = soup.find_all(element, 'cpr-image--focus')
        for x in div:
            left = re.findall(r'left: (.+?)px', x.encode('utf-8'))
            top = re.findall(r'top: (.+?)px', x.encode('utf-8'))
            if left and top:
                return {'cpr_left_top_focus': (left[0], top[0])}

        return

    else:
        return False
