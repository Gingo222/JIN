# -*- coding: utf-8 -*-

from cypressPage import CypressPage
from web_driver.daphne.func2.page_func import *
from web_driver.daphne.func2.CTA_setting import *
from web_driver.daphne.func2.create_report import part
from web_driver.daphne.func2.cta_error import CtaTestCaseError


class Daphne(CypressPage):

    def __init__(self):
        CypressPage.__init__(self)
        self.daphne_branch_list = []
        self.daphne_branch_list_func()
        self.dicom_four()

    def daphne_branch_list_func(self):
        nub = 0

        while True:
            branch = self.is_element_exist((daphne_branch_xpath['top_branch_first']
                                            + str(nub)
                                            + daphne_branch_xpath['top_branch_second']),
                                           key_path='xpath')
            if branch:
                self.daphne_branch_list.append(branch)
            nub += nub

    def dicom_four(self):
        for x in range(len(self.daphne_branch_list)):
            self.driver.execute_script((daphne_branch_xpath['top_branch_first']
                                        + str(x + 1)
                                        + daphne_branch_xpath['top_branch_second']))

            @run_test_func
            def daphne_dicom():
                self.driver.execute_script(daphne_branch_xpath['daphne_dicom'])

            @run_test_func
            def daphne_cpr():
                self.driver.execute_script(daphne_branch_xpath['daphne_cpr'])


            @test_model_except_exception
            def daphne_xsection():
                self.driver.execute_script(daphne_branch_xpath['daphne_xsection'])

            @run_test_func
            def daphne_lumen():
                self.driver.execute_script(daphne_branch_xpath['daphne_lumen_xpath'])


if __name__ == '__main__':
    daphne = Daphne()
