#!usr/bin/env python
# -*- coding:utf-8 _*-


import os
import sys
import time
import re
import csv


pattern = re.compile('All\s+Completed\s+in\s+(\d+\.\d+).*!!')
today = time.strftime("%Y%m%d", time.localtime())
case_output_dir = '/Users/jinjie/staging/output'
log_dir = 'cta.log'
CSV_FILE = 'tester.csv'
body = list()


def get_medical_record_time(date):
    sum, count = 0.0, 0
    os.chdir(case_output_dir)
    case_output_list = os.listdir('./')
    for case_output in case_output_list:
        if date in case_output:
            cat_log_path = os.path.join(os.path.join(case_output_dir, case_output), log_dir)
            if os.path.isfile(cat_log_path):
                with open(cat_log_path, 'r') as f:
                    line = f.readlines()[-1].strip('\n')
                    result = re.findall(pattern, line)
                    if len(result) > 0:
                        body.append([case_output, result[0]])
                        print(case_output, result[0])
                        count = count + 1
                        sum = sum + float(result[0])
    write_csv()
    print('avgtime: {}, sum: {}, count: {} '.format(sum/float(count), sum, count))


def write_csv():
    def init_csv():
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        csv_header = ['case_num', 'time']
        with open(CSV_FILE, 'w+') as csv_file:
            csv_obj = csv.writer(csv_file)
            csv_obj.writerow(csv_header)

    def write_csv_body():
        with open(CSV_FILE, 'a+') as csv_file:
            csv_obj = csv.writer(csv_file)
            csv_obj.writerows(body)

    init_csv()
    write_csv_body()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        date_time = sys.argv[1]
        get_medical_record_time(date_time)
    else:
        get_medical_record_time(today)