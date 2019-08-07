# -*- coding: utf-8 -*-
import os
import sys


report_path = '../template/test_report.html'
reload(sys)
sys.setdefaultencoding('utf-8')


def head():
    with open('../template/test_report.html', 'w') as file_top:
        file_top.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>批量查询对比报告</title>
    <style>span{background-color:lightgreen;}</style>
    <link href="../template/infoCla.css" rel="stylesheet" type="text/css"/>
</head>
    <body style="font-size:13px;"><br>
        <table>
            <thead>
                <tr>
                    <th colspan="5" class = "fff">CTA_Test_Report</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class = "tablesheetwiden2"> 测试页面 </td>
                    <td class = "tablesheetwiden2"> 测试案例 </td>
                    <td class = "tablesheetwiden2"> 冠脉分支 </td>
                    <td class = "tablesheetwiden"> 是否通过 </td>
                    <td class = "tablesheetwiden3"> 错误信息 </td>
                </tr>
        ''')


def bottom():
    with open(report_path, 'a') as file_bottom:
        file_bottom.write('''
           </tbody>
        </table>
    </body>
</html>
''')


def clean_report():
    size = os.path.getsize(report_path)
    if size >= 0:
        try:
            with open(report_path, 'wb') as f:
                f.truncate()
        except:
            print ("clean html error")
            return False
        return True


def part(test_suite, testcase, branch, succ, info):
    with open(report_path, 'a') as file_part:
        file_part.write('''
           <tr>
               <td>{0}</td>
               <td>{1}</td>
               <td>{2}</td>
               <td>{3}</td>
               <td>{4}</td>
           </tr>
    ''' .format(test_suite, testcase, branch, succ, info)
                        )
