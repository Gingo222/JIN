# -*- coding: utf-8 -*-
# k = ["idNo", "idNo", "idNo", "mobileNo", "mobileNo"]
# list_k = ["idNo", "idNo", "idNo"]
# index_k = [0, 1, 2]
# list_v = []
# list_value = ["510114198712133582", "510114198712133583", "510114198712133584", "321", "322"]
# json_a = {"busiData":{"batchNo":"BATCH20171120114552r85bgfm1eQ0","records":[{"entityAuthCode":"dfa","entityAuthDate":"2017-11-20","idNo":"510114198712133582","idType":"0","mobileNo":"18126098065","refMobileNo":"18112345671","refName":"张三","name":"郑冬卉","reasonCode":"01","seqNo":"1"}],"subProductInc":"0001000000001"},"header":{"authCode":"CRT001A2","authDate":"2015-12-02 14:12:14","chnlId":"qhcs-dcs","orgCode":"10000000","transDate":"2017-11-20 11:45:52","transNo":"''' + transNo2 + '''"},"securityInfo":{"userName":"V_PA025_QHCS_DCS","userPassword":"af8f60dd67906ac8287ba38343ee5f6b821ce6d9"}}
# json_b = json_a["busiData"]["records"][0]
# a = json_b.keys()
# b = json_b.values()
# print(a)
# print(b)


# 获取value值
# for x in range(len(list_k)):
#     list_v.append(list_value[index_k[x]])
# print list_v
#
# try:
#     for x in list_k:
#         if json_b[x]:
#             print(json_b[x])
# except Exception as e:
#     print(e)


a = "This is a test"
print a[9:] + a[7:9] + a[4:8] + a[0:4]


