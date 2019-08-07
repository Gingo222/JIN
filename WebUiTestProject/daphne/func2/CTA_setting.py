# -*- coding: utf-8 -*-
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


selection_xpath = {'top_path': '//*[@id="content"]/div/div/section/aside/div/div[1]/section',
                   'mid_path': '/div[',
                   'bottom_path': ']/span'
                   }


branch_xpath = {
    "dicom": "document.getElementsByClassName('dicom-viewer-container')[0].click()",
    "dicom_blood": "document.getElementsByClassName('ant-btn btn-show')[0].click()",
    "dicom_xpath": '//*[@id="content"]/div/div/section/div/div/div[1]/div/div[3]/canvas[1]',
    "dicom_border_xpath": '//*[@id="content"]/div/div/section/div/div/div[1]',
    "dicom_blood_xpath": "(.//*[normalize-space(text()) and normalize-space(.)='Created with Sketch.'])"
                         "[2]/following::button[1]",
    "cpr_xpath": "document.getElementsByClassName('cpr-image-container')[0].click()",
    "cpr_border_xpath": '//*[@id="content"]/div/div/section/div/div/div[3]',
    "cpr_doubleclick_obj": '''(.//*[normalize-space(text()) and normalize-space(.)='WL:'])[2]/following::canvas[1]''',
    "cpr_hide_button": "document.getElementsByClassName('ant-btn btn-show')[3].click()",
    "section_xpath": "document.getElementsByClassName('shortaxis-image')[0].click()",
    "section_border_xpath": '//*[@id="content"]/div/div/section/div/div/div[4]',
    "lumen_xpath": "(.//*[normalize-space(text()) and normalize-space(.)='WL:'])[3]/following::div[18]",
    "lumen_border_xpath": '//*[@id="content"]/div/div/section/div/div/div[5]',
    "success": "document.getElementsByClassName('ant-btn ant-btn straitness-sidebar--report-btn')[0].click()",
    "confirm": "document.getElementsByClassName('ant-btn secondary-btn')[0].click()"
    }


daphne_branch_xpath = {
    "top_branch_first": "document.getElementsByClassName('vessel-selection-bar--item--name')[",
    "top_branch_second": "].click()",
    "daphne_dicom": "document.getElementsByClassName('dicom-viewer-container')[0].click()",
    "daphne_cpr": "document.getElementsByClassName('cpr-image-container')[0].click()",
    "daphne_xsection": "document.getElementsByClassName('shortaxis-image')[0].click()",
    "daphne_lumen_xpath": "(.//*[normalize-space(text()) and normalize-space(.)='WL:'])[3]/following::div[18]"
}


branch_relationship = {
    u"左前降支 LAD": "LAD",
    u"第一对角支 D1": "D1",
    u"第一对角支 D2": "D2",
    u"中间支 RI": "RI",
    u"左回旋支 LCX": "LCX",
    u"第一钝缘支 OM1": "OM1",
    u"第二钝缘支 OM2": "OM2",
    u"左室后支 R-PLB": "R-PLB",
    u"右冠状动脉 RCA": "RCA",
    u"右后降支 R-PDA": "R-PDA"
}