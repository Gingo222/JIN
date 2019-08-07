# -*- coding: utf-8 -*-
import http.client
import json
import numpy as np 

# srv endpoint
ENDPOINT = '10.11.10.131:7010'
conn = http.client.HTTPConnection(ENDPOINT)

# 需要导出的case_num
#case_nums = ['080BF4_080-020_1.2.840.113619.6.80.114374075989539.5865']
case_nums = list(np.load('./latest.npy'))
headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
}

form = {'case_nums': case_nums}
payload = json.dumps(form)

print('Exporting cases:', case_nums)

try:
    conn.request("POST", "/reports/file/export", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
except BaseException as e: 
    print("Error exporting cases:", case_nums)
    print(repr(e))