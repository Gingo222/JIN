# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from service.mockdbsql import selectrep, selectAll, select_route_info,del_route, update_reponseMsg, count_int,\
    selectLogicRepSql, selectLogicKeySql, selectLogicValueSql
from service.uploadcontrol import type_logic
import service.dbsqliteserver as db_server
import json
import ConfigParser


app = Flask(__name__)
bootstrap = Bootstrap(app)
# 设置文件上传大小5mb
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['SECRET_KEY'] = 'hard to guess string'
sqlite_Connect = db_server.sqlite_connect()
cf = ConfigParser.ConfigParser()
cf.read('config/route.conf')
port = cf.getint("routePort", "httpPort")

# 上传接口页面，接口反页面
@app.route('/upload.html', methods=["POST", "GET"])
def index_html():
    message = "pleased to meet you"
    return render_template('test.html', name=message)


# 上传文件接口
@app.route('/uploadFile.do', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        reqtype = request.form.get('reqtype')
        routename = request.form.get('routename')
        reponseMsg = request.form.get('res')
        print(request.form)
        try:
            thekey = (request.form.getlist("theKey"))
            thevalue = (request.form.getlist("theValue"))
            if request.form.get("res"):
                reslist = (request.form.getlist("res"))
            else:
                return "响应内容为空"
        except Exception:
            thekey, thevalue= '', ''
        return type_logic(reqtype, routename, reponseMsg, thekey, thevalue, reslist)
    else:
        return render_template("test.html")


#主页接口
@app.route('/home.html')
def homeIndex():
    return render_template('home.html')


#http动态接口
@app.route('/mock/<name>', methods=["POST", "GET"])
def changeRoute(name):
    sqlLogic = selectLogicKeySql(name)
    keydata = sqlite_Connect.execSqlLogic(sqlLogic)
    if keydata == 'flase':
        return "无此接口"
    if not keydata[0]["thekey"]:
        sql = selectrep(name)
        data = sqlite_Connect.selmsg(sql)
        # sqlite_Connect.closecon()
        if data:
            return data
        else:
            return "无此接口"
    else:
        # 处理请求数据
        thereq = request.get_data()
        if thereq == "":
            return "请求参数为空"
        jsonreq = json.loads(thereq)
        list_k =[]
        # 遍历 keydata ，若 key 包含在请求的 数据中，记下其索引
        keydata = keydata[0]["thekey"].split("-$$-")
        for index, x in enumerate(keydata):
            if x in str(jsonreq["busiData"]["records"][0].keys()):
                list_k.append(index)
        # 获取 value res 的值 通过索引组合查询对应关系
        theresListSql = selectLogicRepSql(name)
        thevauleListSql = selectLogicValueSql(name)
        try:
            # 获取value list
            value_data = sqlite_Connect.execSqlLogic(thevauleListSql)[0]["thevalue"].split("-$$-")
            # 通过list_k 内的索引值取出对应的value值
            for r in list_k:
                if value_data[r] in str(jsonreq["busiData"]["records"][0].values()):
                    res_data = sqlite_Connect.execSqlLogic(theresListSql)[0]["res"].split("-$$-")
                    return res_data[r]
                return "未找到符合逻辑的返回值"

            # for index, y in enumerate(value_data):
            #     if y in str(jsonreq["busiData"]["records"][0]):
            #         list_v.append(index)
            # res_data = sqlite_Connect.execSqlLogic(theresListSql)[0]["res"].split("-$$-")
            # return res_data[list_v[0]]
        #
        except Exception:
            return "error"

# 翻页接口
@app.route('/selectAll.do', methods=['GET', 'POST'])
def selectall():
    try:
        startNum = request.form.get("pageNumber")
        startNum = int(startNum.encode('utf-8'))
        if startNum == 1:
            startNum = startNum - 1
        else:
            startNum = 10*(startNum-1)
    except Exception as e:
        return "startNum未发现"
    else:
        sql = selectAll(startNum)
        data = sqlite_Connect.selAll(sql)
        return data

@app.route('/selectPageNumber.do', methods=['GET', 'POST'])
def selectPageNumber():
    pagenub = count_int()
    datanub = sqlite_Connect.selAll(pagenub)
    datanubjson = json.loads(datanub)
    tolnub = int(datanubjson[0]["tolnub"])
    if (tolnub % 10) == 0:
        pagenub = str(datanub/10)
    else:
        pagenub = str(tolnub/10 + 1)
    return '''{"tolnub":"%s","pagenub":"%s"}'''% (str(tolnub), pagenub)


@app.route('/detail/intId=<name>', methods=["GET", "POST"])
def get_intId_Info(name):
    sql = select_route_info(name)
    data = sqlite_Connect.selcer(sql)
    routeUrl = data['routeUrl']
    responseMsg = data['reponseMsg']
    typeCode = data['type']
    if typeCode == "0":
        typeCode = "http"
    if typeCode == "1":
        typeCode = "https"
    if typeCode == "2":
        typeCode = "XML"
    return render_template('detail.html', routeUrl=routeUrl, reponseMsg=responseMsg, typeCode=typeCode)

#修改接口页面接口
@app.route('/updateInt/intId=<name>', methods=["GET", "POST"])
def update_intId(name):
    sql = select_route_info(name)
    data = sqlite_Connect.selcer(sql)
    routeUrl = data['routeUrl']
    reponseMsg = data['reponseMsg']
    typeCode = data['type']
    creater = data["creater"]
    if typeCode == "0":
        typeCode = "http"
    if typeCode == "1":
        typeCode = "https"
    if typeCode == "2":
        typeCode = "XML"
    return render_template('updateInt.html', routeUrl=routeUrl, typeCode=typeCode, creater=creater)


@app.route("/logicInfo", methods=["POST", "GET"])
def logicInfo():
    routeName = request.form.get("routeName")
    sql = select_route_info(routeName)
    data = sqlite_Connect.selcer(sql)
    theKey = data['thekey']
    theValue = data['thevalue']
    if not theKey:
        theKey = []
        theValue = []
    else:
        theKey = theKey.encode('utf-8').split("-$$-")
        theValue = theValue.encode('utf-8').split("-$$-")
    try:
        res = data['res'].encode('utf-8').split("-$$-")
    except Exception as e:
        res = []
    finally:
        addData = {}
        addData["theKey"] = theKey
        addData["theValue"] = theValue
        addData["res"] = res
        return json.dumps(addData, ensure_ascii=False)


@app.route("/delIntId", methods=["POST"])
def delInt():
    name = request.form.get("dsInt")
    sql = del_route(name)
    if sqlite_Connect.selcer(sql) == "del":
        return "success"
    return "接口删除错误"


#修改接口接口
@app.route("/updateInterFace.do", methods=["POST", "GET"])
def updateInterFace():
    routeName = request.form.get("routename")
    res = request.form.getlist("res")
    if not res:
        return "响应参数为空"
    theKey = request.form.getlist("theKey")
    theValue = request.form.getlist("theValue")
    thekey = '-$$-'.join(theKey)
    thevalue = '-$$-'.join(theValue)
    res = '-$$-'.join(res)
    sql = update_reponseMsg(routeName, thekey, thevalue, res )
    data = sqlite_Connect.selcer(sql)
    if data == "del":
        return "修改接口成功"
    return "修改接口失败"


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=port)

