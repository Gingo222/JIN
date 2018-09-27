# -*- coding: utf-8 -*-


class CtaTestCaseError(Exception):

    def __init__(self, errorInfo):
        super(CtaTestCaseError).__init__(self, errorInfo)
        self.errorinfo = errorInfo

    def __str__(self):
        return self.errorinfo
