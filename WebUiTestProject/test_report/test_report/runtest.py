# -*- coding: utf-8 -*-

import unittest
import time
from test_case import HTMLTestRunner
from test_case import test_job1

suite = unittest.TestSuite()
suite.addTest(test_job1.JobTest('test_Login'))
now = time.strftime("%Y-%m-%M-%H_%M_%S",time.localtime(time.time()))
fp = open("report/"+now+".html", 'wb')
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='test result', description='result:')
runner.run(suite)
fp.close()
