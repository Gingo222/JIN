# -*- coding: utf-8 -*-
import requests,sys,xlrd,os,time


class ubprd(object):
    # 接口地址
    host = 'http://qhcs-cust-stg.paic.com.cn'
    host_index = host + '/cust/O2sCust/index.html'
    host_login = host + '/cust/O2sCust/login/login.do'
    host_validotp = host + '/cust/O2sCust/login/isMobilenoVerifyLegalForLogin.do'
    # 请求查询接口
    host_post_formdata = host + '/cust/o2sCust/universalQuery/queryProducts.do'
    # 下载接口
    host_download = host + '/cust/o2sCust/universalQuery/downResultExcel.do?batchId='
    host_refresh = host + '/cust/o2sCust/universalQuery/queryCenterRefresh.do'
    host_queryUserPrds = host+'/cust/o2sCust/universalQuery/queryUserPrds.do'
    host_get48hoursBatchSum = host +'/cust/o2sCust/universalQuery/get48hoursBatchSum.do'
    data_validotp = {'phoneVerifyCode': '1111'}

    def login(self):
        data_login = {'userAcct': 'jinjietest001@qq.com',
                  'password': '1111aaaa',
                  'validCode': '1111'}
        s = requests.session()
        html = s.get(ubprd.host_index)
        s.post(ubprd.host_login, data=data_login)
        # otp登陆
        s.post(ubprd.host_validotp, data=ubprd.data_validotp)
        return s

    def req(self,s,excelname,PrdidR):
        download_address = []
        fileopen = open('./testTemplate/' + excelname, "rb")
        files = {'file': (excelname,
                          fileopen,
                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                          )
                 }
        subProductId = '""'
        model = ''
        batchType = '1'

        if PrdidR == '53A2B67D87D46582E053060B1F0AF477':
            subProductId = '"basic"'

        if PrdidR == '53A2B67D87D36582E053060B1F0AF477':
            subProductId = '"professional"'

        if PrdidR == '53A2B67D87C06582E053060B1F0AF477':
            model = '1'

        #判断一鉴通类型
        if PrdidR in [
            '53A2B67D87C16582E053060B1F0AF477',
            '53A2B67D87C46582E053060B1F0AF477',
            '53A2B67D87C66582E053060B1F0AF477',
            '4EAD7BB23D5B406FE053060B1F0A65C3',
            '53A2B67D87C86582E053060B1F0AF477',
            '53A2B67D87C76582E053060B1F0AF477',
            '53A2B67D87C96582E053060B1F0AF477',
            '53A2B67D87C26582E053060B1F0AF477',
            '53A2B67D87C56582E053060B1F0AF477',
            '4EAD86A89A4F9041E053060B1F0A71E9',
            '53A2B67D87D06582E053060B1F0AF477',
            '53A2B67D87C36582E053060B1F0AF477'
            ]:
            subProductId = '"0000000000000001"'
            batchType = '2'
            #好信一鉴通-工作单位验证
            if PrdidR == '53A2B67D87C66582E053060B1F0AF477':
                subProductId = '"0000000000000100"'
            #好信一鉴通-地址验证
            if PrdidR == '53A2B67D87C46582E053060B1F0AF477':
                subProductId = '"0000000000000010"'
            # 车辆驾驶证状态查询特殊处理,好信一鉴通-行驶证核查
            if PrdidR in ('4EAD7BB23D5B406FE053060B1F0A65C3',
                               '4EAD86A89A4F9041E053060B1F0A71E9'):
                subProductId = '""'
            #好信一鉴通-房产验证
            if  PrdidR == '53A2B67D87C86582E053060B1F0AF477':
                subProductId = '"0000000001000000"'
                batchType = '2'
            #一鉴通手机验证判断
            if PrdidR == '53A2B67D87C76582E053060B1F0AF477':
                subProductId = '"0000001000000000"'
                batchType = '2'
            #一鉴通银行卡鉴全
            if PrdidR == '53A2B67D87C96582E053060B1F0AF477':
                subProductId = '""'
                batchType = '2'
            #一鉴通学历验证
            if PrdidR == '53A2B67D87C26582E053060B1F0AF477':
                subProductId = '"0000000100000000"'
            #好信一鉴通-关系人验证
            if PrdidR == '53A2B67D87C56582E053060B1F0AF477':
                subProductId = '"0000000000010000"'
            #车辆和行驶证状态验证
            if PrdidR in ( '53A2B67D87D06582E053060B1F0AF477',
                           '53A2B67D87CF6582E053060B1F0AF477'):
                subProductId = '""'
            #车辆验证
            if PrdidR == '53A2B67D87C36582E053060B1F0AF477':
                subProductId = '"0000000000100000"'

        data = {'fileDesc': '',
                'usrPrdIds': '[{"usrPrdId":' + '"' + (PrdidR) + '"' +
                             ',"subProductId":' + subProductId + ',' +
                             '"model":"' + model + '"}]',
                'queryType': 'batch',
                'batchType': batchType
                }

        try:
            r = s.post(url = ubprd.host_post_formdata, files = files, data = data)
            time.sleep(1)
            rr = r.json()
            try:
                batchId_re = rr['record']['records'][0]['idO2QueryCenterBatchSum']
                status = rr['record']['records'][0]['status']
                while status == '3':
                    data_refresh = {'queryType':'batch',
                                    'isBatch':'1',
                                    'idO2QueryCenterBatchSum':batchId_re}
                    #调用刷新接口
                    ref = s.post(url=ubprd.host_refresh,data=data_refresh)
                    refj = ref.json()
                    if refj['errCode'] == 'E000000':
                    #调用48小时接口
                        data_q = {'queryType':'1'}
                        hur = s.post(url=ubprd.host_get48hoursBatchSum,data=data_q)
                        hurj = hur.json()
                        status = hurj['record']['records'][0]['status']
                        if status == ('0'or '4'):
                            if sys.version_info[0] == 2:
                                batchId = batchId_re.encode('utf-8')
                                download_address2 = ubprd.host_download + batchId
                                download_address.append(download_address2)
                            else:
                                download_address2 = ubprd.host_download + batchId_re
                                download_address.append(download_address2)

                        else:
                            print ('status :',status,'continue')

                    else:
                        print('refresh failed ,stop range')
                        return False

                if status == ('0'or '4'):
                    if sys.version_info[0] == 2:
                        batchId = batchId_re.encode('utf-8')
                        download_address2 = ubprd.host_download + batchId
                        download_address.append(download_address2)
                    else:
                        download_address2 = ubprd.host_download + batchId_re
                        download_address.append(download_address2)

                if status == '1':
                    if PrdidR in ():
                        print (excelname,'ub request success ,but something error in dcs')
                        return False

                    else:
                        if sys.version_info[0] == 2:
                            batchId = batchId_re.encode('utf-8')
                            download_address2 = ubprd.host_download + batchId
                            download_address.append(download_address2)
                        else:
                            download_address2 = ubprd.host_download + batchId_re
                            download_address.append(download_address2)

                else:
                    print ('reponse status error,status = 2')

                    return False

            except Exception as e:
                print ('request error: ',e)

        except Exception as e:
            print ('match error:',e)
            return False

        fileopen.close()
        return download_address

    def choosePrd(self,x):
        Prdid = [
            '53A2B67D87C06582E053060B1F0AF477',
            '53A2B67D87D96582E053060B1F0AF477',
            '53A280DAB0196650E053060B1F0AFD96',
            '53A280DAB0176650E053060B1F0AFD96',
            '53A280DAB0166650E053060B1F0AFD96',
            '53A280DAB0216650E053060B1F0AFD96',
            '53F14B0F3E246B19E053060B1F0ABB2A',
            '53A2B67D87D16582E053060B1F0AF477',
            '53A2B67D87CD6582E053060B1F0AF477',
            '53A280DAB01B6650E053060B1F0AFD96',
            '53A280DAB01E6650E053060B1F0AFD96',
            '53A2B67D87D26582E053060B1F0AF477',
            '53A280DAB0206650E053060B1F0AFD96',
            '53A280DAB0226650E053060B1F0AFD96',
            '53A2B67D87D36582E053060B1F0AF477',
            '53A2B67D87D46582E053060B1F0AF477',
            '53F230E7CD861691E053060B1F0A435A',
            # 一鉴通
            '53A2B67D87C16582E053060B1F0AF477',
            '53A2B67D87C46582E053060B1F0AF477',
            '53A2B67D87C66582E053060B1F0AF477',
            '53A2B67D87C86582E053060B1F0AF477',
            '53A2B67D87C76582E053060B1F0AF477',
            '53A2B67D87C96582E053060B1F0AF477',
            '53A2B67D87C26582E053060B1F0AF477',
            '53A2B67D87C56582E053060B1F0AF477',
            #异步产品
            '53A2B67D87DA6582E053060B1F0AF477',
            '53A2B67D87D06582E053060B1F0AF477',
            '53A2B67D87CF6582E053060B1F0AF477',
            '53A2B67D87C36582E053060B1F0AF477',

        ]
        Prdid2 = [
            '53F230E7CD861691E053060B1F0A435A'
        ]
        return Prdid[x]

    def prdlist(self,str):
        prdlist = {
            'credoo2.0.xlsx': '好信度2.0(小贷评分卡)',
            'Risktip2.0.xlsx': '风险度提示2.0版(基础版)',
            'passengerTravelinfo.xlsx': '航客出行信息查询',
            'phoneVerification.xlsx': '手机验证（手机号码状态及在网时长）',
            'phoneVerification2.xlsx': '手机验证（手机号证件姓名验证）',
            'drivingScore.xlsx': '驾驶分',
            'badInformation.xlsx': '不良信息',
            'credooSeniorExecutive.xlsx': '好信高管通',
            'educationQuery.xlsx': '学历查询',
            'credooMoblieInfo.xlsx': '好信手机综合资讯',
            'credooGoodFaithTrack.xlsx': '好信信用轨迹',
            'AntiFraudRisk_ip_moblie.xlsx': '反欺诈风险认证ip与手机查询',
            'idQuery.xlsx': '身份多项查询',
            'addressPass.xlsx': '地址通',
            'credoo.xlsx': '好信度（专业版）',
            'credooRegularloan.xlsx': '好信常贷客（基础版）',
            'credooCarrental.xlsx': '好信租车分',
            # 一鉴通
            'one_idvalid.xlsx': '好信身份验证',
            'one_addressvalid.xlsx': '好信一鉴通-地址验证',
            'one_workbussValid.xlsx': '好信一鉴通-工作单位验证',
            'one_houseValid.xlsx': '好信一鉴通-房产验证',
            'one_moblieValid.xlsx': '好信一鉴通-手机验证',
            'one_bankcardvalid.xlsx': '一鉴通银行卡鉴权',
            'one_educationvalid.xlsx': '好信一鉴通-学历验证',
            'one_relationmanValid.xlsx': '好信一鉴通-关系人验证',
            # 异步产品
            'one_dirverbStatus.xlsx': '驾驶证状态查询',
            'one_carAndBookv.xlsx': '车辆和行驶证状态验证',
            'one_runCardV.xlsx': '行驶证核查',
            'one_carValid.xlsx': '车辆验证【车辆信息】',
        }
        if  str == '1':
            return len(prdlist)
        else:
            return prdlist[str]

    def chooseExl(self,x):
        name = [
            'credoo2.0.xlsx',
            'Risktip2.0.xlsx',
            'passengerTravelinfo.xlsx',
            'phoneVerification.xlsx',
            'phoneVerification2.xlsx',
            'drivingScore.xlsx',
            'badInformation.xlsx',
            'credooSeniorExecutive.xlsx',
            'educationQuery.xlsx',
            'credooMoblieInfo.xlsx',
            'credooGoodFaithTrack.xlsx',
            'AntiFraudRisk_ip_moblie.xlsx',
            'idQuery.xlsx',
            'addressPass.xlsx',
            'credoo.xlsx',
            'credooRegularloan.xlsx',
            'credooCarrental.xlsx',
            #一鉴通
            'one_idvalid.xlsx',
            'one_addressvalid.xlsx',
            'one_workbussValid.xlsx',
            'one_houseValid.xlsx',
            'one_moblieValid.xlsx',
            'one_bankcardvalid.xlsx',
            'one_educationvalid.xlsx',
            'one_relationmanValid.xlsx',
            #异步产品
            'one_dirverbStatus.xlsx',
            'one_carAndBookv.xlsx',
            'one_runCardV.xlsx',
            'one_carValid.xlsx',
        ]
        name2 = [
            'credooCarrental.xlsx'
        ]
        return name[x]

    def downloadfile(self,download_address,s,excel_name):
        for x in download_address:
            downloadf = s.get(x)
            with open('./downloadfile/d_'+ excel_name ,'wb') as df:
                df.write(downloadf.content)

    def compareExcel(self, excel_name):
        downloadfile_address = './downloadfile/d_'+excel_name
        print(downloadfile_address)
        try:
            exl_d = xlrd.open_workbook(downloadfile_address)
        except Exception :
            print(excel_name,'file open error')
            return False

        originfile_address = './originFilename/' + excel_name
        exl_o = xlrd.open_workbook(originfile_address)
        table_d = exl_d.sheets()[0]
        table_o = exl_o.sheets()[0]

        nrows_d = table_d.nrows
        ncols_d = table_d.ncols

        nrows_o = table_o.nrows
        ncols_o = table_o.ncols

        if nrows_d != nrows_o:
            print (excel_name,"File Exception")
            return False

        if ncols_d != ncols_o:
            print (excel_name,"File Exception")
            return False

        counterrortimes = 0
        mgt = ubprd()
        prd_name = mgt.prdlist(excel_name)
        result = 'Same'
        result2 = 'Different'
        for y in range(ncols_d):
            for x in range(nrows_d):
                cell_d = table_d.cell(x,y).value
                cell_o = table_o.cell(x,y).value
                if cell_d != cell_o:
                    diffpostion = '''"%s",row:"%d",col:"%d",compare different'''%(excel_name,x+1,y+1)
                    counterrortimes = counterrortimes+1
                    origin = cell_o
                    new = cell_d
                    if sys.version_info[0] == 2:
                        origin = cell_o.encode('utf-8')
                        new = cell_d.encode('utf-8')
                    diffmess = '''origin: <span> "%s" </span>,new:<span> "%s" </span> '''%(origin,new)
                    print (diffpostion)
                    print (diffmess)
                    with open('./message.html','a') as file:
                        file.write('''
       <tr>
           <td>%s</td>
           <td>%s</td>
           <td>%s</td>
           <td>%s</td>
           <td>%s</td>
       </tr>
'''%(prd_name,excel_name,result2,diffpostion,diffmess)
                                   )
        if counterrortimes == 0:
            with open('./message.html', 'a') as file:
                file.write('''
       <tr>
           <td>%s</td>
           <td>%s</td>
           <td>%s</td>
           <td>%s</td>
           <td>%s</td>
       </tr>
            ''' % (prd_name,excel_name,result,'','')
                           )

        print (excel_name ,'compare finish')
        return True

    def html_top(self,step):
        if step =='1':
            with open('./message.html','w') as file:
                file.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>批量查询对比报告</title>
    <style>span{background-color:lightgreen;}</style>
    <link href="infoCla.css" rel="stylesheet" type="text/css"/>
</head>
    <body style="font-size:13px;"><br>

        <table>
            <thead>
                <tr>
                    <th colspan="5" class = "fff">批量对比汇总</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class = "tablesheetwiden7"> 产品名 </td>
                    <td class = "tablesheetwiden2"> 产品excel名 </td>
                    <td class = "tablesheetwiden6"> 对比是否一致 </td>
                    <td class = "tablesheetwiden"> 不一致位置 </td>
                    <td class = "tablesheetwiden5"> 对比错误信息 </td>
                </tr>
'''
                        )

    def html_down(self):
        with open('./message.html', 'a') as file:
            file.write('''
           </tbody>
        </table>
    </body>
</html>
'''
                       )

    def html1(self):
        size=os.path.getsize('./message.html')
        if size >= 0:
            try:
                with open('./message.html','wb') as f:
                    f.truncate()
            except Exception as e:
                print ("clean html error")
                return False
            return 'pass'

    def runit(self):
        tt = ubprd()
        ss = tt.login()
        tt.html1()
        tt.html_top(step='1')
        str = '1'
        lenlist = tt.prdlist(str)
        for x in range(lenlist):
            excel_name = tt.chooseExl(x)
            Prd_name = tt.choosePrd(x)
            download_address = tt.req(ss,excel_name,Prd_name)
            if download_address == False:
                continue
            tt.downloadfile(download_address,ss,excel_name)
            if tt.compareExcel(excel_name) == False:
                continue
        tt.html_down()

if __name__ == '__main__':
    y = ubprd()
    y.runit()





'''
同步产品：
'53A2B67D87C06582E053060B1F0AF477',          1 credoo2.0     			   好信度2.0(小贷评分卡)
'53A2B67D87D96582E053060B1F0AF477',          2 Risktip2.0				   风险度提示2.0版(基础版)
'53A280DAB0196650E053060B1F0AFD96',          3 passengerTravelinfo     航客出行信息查询
'53A280DAB0176650E053060B1F0AFD96',          4 phoneVerification       手机验证（手机号码状态及在网)
'53A280DAB0166650E053060B1F0AFD96',          5 phoneVerification2      手机验证（手机号证件姓名验证）
'53A280DAB0216650E053060B1F0AFD96',          6 drivingScore            驾驶分
'53F14B0F3E246B19E053060B1F0ABB2A',          7 badInformation          不良信息
'53A2B67D87D16582E053060B1F0AF477',          8 credooSeniorExecutive   好信高管通
'53A2B67D87CD6582E053060B1F0AF477',          9 educationQuery          学历查询
'53A280DAB01B6650E053060B1F0AFD96',          10 credooMoblieInfo       好信手机综合资讯
'53A280DAB01E6650E053060B1F0AFD96',          11 credooGoodFaithTrack   好信信用轨迹
'53A2B67D87D26582E053060B1F0AF477',          12 AntiFraudRisk_ip_moblie反欺诈风险认证ip与手机查询
'53A280DAB0206650E053060B1F0AFD96',          13 idQuery                身份多项查询
'53A280DAB0226650E053060B1F0AFD96',          14 addressPass            地址通
'53A2B67D87D36582E053060B1F0AF477',#特殊判断  16 credoo                  好信度（专业版）
'53A2B67D87D46582E053060B1F0AF477',#特殊判断  17 credooRegularloan       好信常贷客（基础版）
#'53A2B67D87DB6582E053060B1F0AF477',          18 netLoanRiskDegree      网贷风险度查询  （查询无权限）
'53F230E7CD861691E053060B1F0A435A',          19 credooCarrental		   好信租车分

一鉴通产品：
'one_idvalid.xlsx',			  1 one_idvalid             好信身份验证
'one_addressvalid.xlsx',     2 one_addressvalid        好信一鉴通-地址验证
'one_workbussValid.xlsx',    3 one_workbussValid	     好信一鉴通-工作单位验证
'one_houseValid.xlsx',       4 one_houseValid          好信一鉴通-房产验证
'one_moblieValid.xlsx',      5 one_moblieValid		     好信一鉴通-手机验证
'one_bankcardvalid.xlsx',    6 one_bankcardvalid	     一鉴通银行卡鉴权
'one_educationvalid.xlsx',   7 one_educationvalid	     好信一鉴通-学历验证
'one_relationmanValid.xlsx', 8 one_relationmanValid	   好信一鉴通-关系人验证

异步产品：
Z06024   驾驶证状态查询          53A2B67D87DA6582E053060B1F0AF477          one_dirverbStatus
#Z06055   车产查验
Z06037   车辆和行驶证状态验证      53A2B67D87D06582E053060B1F0AF477     one_carAndBookv.xlsx
Z06051   行驶证核查               53A2B67D87CF6582E053060B1F0AF477      one_runCardV.xlsx
Z06023   车辆验证【车辆信息】      53A2B67D87C36582E053060B1F0AF477      one_carValid

特殊返回产品：
Z06054   好信法院通高级版（个人）   53A280DAB0246650E053060B1F0AFD96
Z06121   好信法院诉讼信息
Z06110   好信法院通高级版（企业）
'''