import unittest
import time
import shutil
import os
from web_driver.test_case import HTMLTestRunner
from web_driver.testfile import classmethodtest

suite = unittest.TestSuite()
suite.addTest(classmethodtest.CTest("test_login"))
now = time.strftime("%Y-%m-%M-%H_%M_%S", time.localtime(time.time()))
shutil.rmtree("../report")
shutil.rmtree("../picture")
os.mkdir('../report')
os.mkdir("../picture")
fp = open("../report/"+now+".html", 'wb')
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='test result', description='result:')
runner.run(suite)
fp.close()

