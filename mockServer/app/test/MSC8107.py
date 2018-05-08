# -*- coding: utf-8 -*-
import requests
import hashlib
import random
import base64
import json
import time

#url = "http://103.28.215.128:8080/api/query"
url = "http://116.62.155.23/query"
# url = "http://localhost:28010/api/query"
appId = "test"
transNo2 = str(random.randint(10000000, 99999999999))

transNo = "testMSC8107DMZ201708151616052399912345"

intFcId = {
    "一鉴通": "MSC8107DMZ",
    "常贷客": "MSC8037",
    "好信度": "MSC8005",
    "反风险欺诈": "MSC8075",
    "地址通": "MSC8007",
    "法院通个人": "MSC8178",
    "法院通个人异步": "MSC8179",
    "定制化模型": "MSC8220"
    }

reqArr = {
    "一鉴通": '''[{"busiData":{"batchNo":"BATCH20171120114552r85bgfm1eQ0","records":[{"entityAuthCode":"dfa","entityAuthDate":"2017-11-20","idNo":"510114198712133582","idType":"0","mobileNo":"18126098065","refMobileNo":"18112345671","refName":"张三","name":"郑冬卉","reasonCode":"01","seqNo":"1"}],"subProductInc":"0001000000001"},"header":{"authCode":"CRT001A2","authDate":"2015-12-02 14:12:14","chnlId":"qhcs-dcs","orgCode":"10000000","transDate":"2017-11-20 11:45:52","transNo":"''' + transNo2 + '''"},"securityInfo":{"userName":"V_PA025_QHCS_DCS","userPassword":"af8f60dd67906ac8287ba38343ee5f6b821ce6d9"}}]''',
    "常贷客": '''[{"busiData":{"batchNo":"BATCH20180102020144IsIUGpcQTFW","records":[{"idNo":"320116198108152944","entityAuthDate":"2016-09-10","idType":"0","seqNo":"001","name":"宰晓卉","reasonCode":"99","entityAuthCode":"11111"}]},"header":{"authCode":"CRT001A2","authDate":"2015-12-02 14:12:14","chnlId":"qhcs-dcs","orgCode":"10000000","transDate":"2017-11-20 11:45:52","transNo":"'''+transNo2+'''"},"securityInfo":{"userName":"V_PA025_QHCS_DCS","userPassword":"af8f60dd67906ac8287ba38343ee5f6b821ce6d9"}}]''',
    "好信度": '''[{"busiData":{"batchNo":"BATCH20180102100114Yp8hHphkkGs","records":[{"cardNo":"54564564564645","entityAuthDate":"2018-02-01","idNo":"310105198110013221","idType":"0","seqNo":"1","name":"哈好","reasonNo":"01","entityAuthCode":"1111","mobileNo":"15658987587"}]},"header":{"authCode":"CRT001A2","authDate":"2015-12-02 14:12:14","chnlId":"qhcs-dcs","orgCode":"10000000","transDate":"2017-11-20 11:45:52","transNo":"'''+transNo2+'''"},"securityInfo":{"userName":"V_PA025_QHCS_DCS","userPassword":"af8f60dd67906ac8287ba38343ee5f6b821ce6d9"}}]''',
    "反风险欺诈": '''[{"busiData":{"batchNo":"BATCH20180102101558iBLkNONSJdD","records":[{"entityAuthDate":"2018-01-24","idNo":"310105198110013221","idType":"0","seqNo":"1","name":"阿*达","reasonNo":"01","entityAuthCode":"11111","mobileNo":"15689875421","ip":"10.22.25.122"}]},"header":{"authCode":"CRT001A2","authDate":"2015-12-02 14:12:14","chnlId":"qhcs-dcs","orgCode":"10000000","transDate":"2017-11-20 11:45:52","transNo":"'''+transNo2+'''"},"securityInfo":{"userName":"V_PA025_QHCS_DCS","userPassword":"af8f60dd67906ac8287ba38343ee5f6b821ce6d9"}}]''',
    "地址通": '''[{"busiData":{"batchNo":"BATCH20180102101758Gs3RMISeQUF","records":[{"entityAuthDate":"2018-01-16","idNo":"310105198110013221","idType":"0","address":"按时打算","seqNo":"1","name":"啊*","reasonNo":"01","entityAuthCode":"1111","mobileNo":"18656565981"}]},"header":{"authCode":"CRT001A2","authDate":"2015-12-02 14:12:14","chnlId":"qhcs-dcs","orgCode":"10000000","transDate":"2017-11-20 11:45:52","transNo":"'''+transNo2+'''"},"securityInfo":{"userName":"V_PA025_QHCS_DCS","userPassword":"af8f60dd67906ac8287ba38343ee5f6b821ce6d9"}}]''',
    "法院通个人": '''[{"busiData":{"batchNo":"BATCH20180102102103crnMOX2fCP7","records":[{"idNo":"310105198110013221","entityAuthDate":"2018-01-17","idType":"0","range":"100","seqNo":"1","reasonCode":"01","entityAuthCode":"1111","entityName":"阿达撒"}]},"header":{"authCode":"CRT001A2","authDate":"2015-12-02 14:12:14","chnlId":"qhcs-dcs","orgCode":"10000000","transDate":"2017-11-20 11:45:52","transNo":"'''+transNo2+'''"},"securityInfo":{"userName":"V_PA025_QHCS_DCS","userPassword":"af8f60dd67906ac8287ba38343ee5f6b821ce6d9"}}]''',
    "法院通个人异步": '''[{"busiData":{"batchNo":"BATCH20180102102103crnMOX2fCP7","records":[{"dataId":"28DEBE31CAAB69901862F235EB3002C7","dataType":"0","queryId":"61C8DCFC1CF384AAE053060B1F0A5A20","searchTransNo":"58558401418","seqNo":"217862762862882","reasonCode":"01","busiDesc":"1111",}]},"header":{"authCode":"CRT001A2","authDate":"2015-12-02 14:12:14","chnlId":"qhcs-dcs","orgCode":"10000000","transDate":"2017-11-20 11:45:52","transNo":"81997457106"},"securityInfo":{"userName":"V_PA025_QHCS_DCS","userPassword":"af8f60dd67906ac8287ba38343ee5f6b821ce6d9"}}]''',
    "定制化模型": '''[{"busiData":{"batchNo":"BATCH20180102100114Yp8hHphkkGs","records":[{"idNo":"510114198712133582","idType":"0","name":"郑冬卉","mobileNo":"18126098065","model":"M1","reasonNo":"01","entityAuthCode":"1111","entityAuthDate":"2018-02-01","seqNo":"1"}]},"header":{"authCode":"CRT001A2","authDate":"2015-12-02 14:12:14","chnlId":"qhcs-dcs","orgCode":"10000000","transDate":"2017-11-20 11:45:52","transNo":"'''+transNo2+'''"},"securityInfo":{"userName":"V_PA025_QHCS_DCS","userPassword":"af8f60dd67906ac8287ba38343ee5f6b821ce6d9"}}]'''
    }

inputIntId = str(raw_input("intId:"))
appSecret = "123456789asdfghjkl123456789asdfghjkl"
allData = appId + intFcId[inputIntId] + transNo + appSecret
sign = hashlib.sha256(allData).hexdigest()
sign = base64.b64encode(sign).upper()
# sign = 'MWFHN2M4ZTLHNZK4MTE1ZDE1ZDRIZDDKMDMYZJBMZTUZZJM1NTI3ODQ3YWJMMGVJNDE5ZTUXMDRJMZRMYTMWZQ=='
formData = {
    "appId": "test",
    "transNo": transNo,
    "sig": sign,
    "version": "1.0",
    "intfcId": intFcId[inputIntId],
    "reqArr": reqArr[inputIntId]
    }

print(url)
print(formData)
response = requests.post(url=url, data=formData).text
print "response:", response
reponse = json.loads(response)
if intFcId[inputIntId] == "MSC8178":
    try:
        queryId = response["records"]["busiData"]["records"][0]["queryId"]
        transNo = response["records"]["header"]["transNo"]
        dataId = response["records"]["busiData"]["records"][0]["judgeDocs"][0]["judgeId"]
        otherData = '''{"busiData":{"batchNo":"BATCH20180102102103crnMOX2fCP7","records":[{"dataId":"''' + dataId + '''","dataType":"0","queryId":"''' + queryId + '''","searchTransNo":"''' + transNo + '''","seqNo":"217862762862882","reasonCode":"01","busiDesc":"1111"}]},"header":{"authCode":"CRT001A2","authDate":"2015-12-02 14:12:14","chnlId":"qhcs-dcs","orgCode":"10000000","transDate":"2017-11-20 11:45:52","transNo":"''' + transNo + '''"},"securityInfo":{"userName":"V_PA025_QHCS_DCS","userPassword":"af8f60dd67906ac8287ba38343ee5f6b821ce6d9"}}'''
        formData["reqList"] = otherData
        formData["intfcId"] = "MSC8179"
        allData = appId + "MSC8179" + transNo + appSecret
        otherSign = hashlib.sha256(allData).hexdigest()
        otherSign = base64.b64encode(otherSign).upper()
        formData["sig"] = otherSign
        otherResponse = requests.post(url=url, data=formData).text
        print otherResponse
    except Exception as e:
        print e

