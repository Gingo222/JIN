# -*- coding: utf-8 -*-

import unittest
import time
import shutil
import os
from test_case import HTMLTestRunner, CypressUiTest

suite = unittest.TestSuite()
suite.addTest(CypressUiTest.JobTest('test_Login'))
suite.addTest(CypressUiTest.JobTest('test_Operate'))
suite.addTest(CypressUiTest.JobTest('test_Coronary_Info'))
now = time.strftime("%Y-%m-%M-%H_%M_%S", time.localtime(time.time()))
shutil.rmtree("report")
shutil.rmtree("picture")
os.mkdir('report')
os.mkdir("picture")
fp = open("report/"+now+".html", 'wb')
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='test result', description='result:')
runner.run(suite)
fp.close()
CypressUiTest.JobTest.del_file_info()
print("finish")