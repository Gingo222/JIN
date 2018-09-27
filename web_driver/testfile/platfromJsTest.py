# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


class HeadlessChromeDriver(object):
    _chrome_options = Options()
    _chrome_options.add_argument('--headless')
    _chrome_options.add_argument('--disable-gpu')
    _chrome_options.add_argument('--no-sandbox')
    _chrome_options.add_argument('window-size=1920x3000')
    _cdriver = "../chrome_driver/chromedriver"
    os.environ["webdriver.chrome.driver"] = _cdriver

    def __init__(self):
        opener = webdriver.Chrome(chrome_options=HeadlessChromeDriver._chrome_options,
                                  executable_path='../chrome_driver/chromedriver')
        opener.get('http://103.211.47.130:70/')
        print(1)


def test_func(func):
    def run(a):
        func(a)
        print('aa')
        return str(a)
    return run


@test_func
def go(a):
    print(a)

go('a')
