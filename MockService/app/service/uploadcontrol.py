# -*- coding: utf-8 -*-
import os
from flask import request
from mockdbsql import selectrouteurl, inserthttps, inserthttp, insertHttpWithLogicSql
import dbsqliteserver as db_server
import ConfigParser


# 设置允许上传的文件类型
cf = ConfigParser.ConfigParser()
cf.read("config/route.conf")
ALLOWED_EXTENSIONS = cf.get("ALLOWED_EXTENSIONS", "ALLOWED_EXTENSIONS")
UPLOAD_FOLDER = cf.get("UPLOAD_FOLDER", "UPLOAD_FOLDER")
UPLOAD_KEYFOLDER = cf.get("UPLOAD_KEYFOLDER", "UPLOAD_KEYFOLDER")
sqlite_connect = db_server.sqlite_connect()


# 检查文件类型是否合法
def allowed_file(filename):
    # 判断文件的扩展名是否在配置项ALLOWED_EXTENSIONS中
    if '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return True
    else:
        return "文件格式错误"

def type_logic(reqtype, routename, reponseMsg, thekey, thevalue , res):
    if reqtype == 'HTTPS':
        # 获取上传过来的文件对象
        file = request.files['file']
        keyword = request.form.get('keyword')
        reqtypehttps = '1'
        if file:
            # 判断文件合法
            allowfile = allowed_file(file.filename)
            sqlite_connect = db_server.sqlite_connect()
            sql = selectrouteurl(routename)
            if sqlite_connect.selectrouteurl(sql) == False:
                return "接口已存在"
            if len(keyword) == 0:
                return "秘钥长度不符合规范"
            if allowfile !=True:
                return "文件格式不符合规范"
            if allowfile == True and len(keyword) > 0:
                UPLOAD_FOLDER2 = UPLOAD_FOLDER + "server.crt"
                if os.path.exists(UPLOAD_FOLDER2):
                    os.remove(UPLOAD_FOLDER2)
                if os.path.exists(UPLOAD_KEYFOLDER + "server.key"):
                    # 保存密码至key文件
                    with open(UPLOAD_KEYFOLDER + "server.key", "w+") as fp:
                        fp.write(keyword)
                # 执行保存文件至服务器地址
                file.save(os.path.join(UPLOAD_FOLDER, "server.crt"))
                # 执行 证书,routeurl,reponseMsg,type,加进mysql
                fp = open(UPLOAD_FOLDER + "server.crt", "r")
                fileInfo = fp.read()
                inssertsql = inserthttps(reqtypehttps, routename, reponseMsg, keyword, fileInfo)
                sqlite_connect.inserthttps(inssertsql)
                sqlite_connect.closecon()
                message = "创建接口成功!"
                data = '''{"message":"%s"}''' % format(message)
                return data
        else:
            message = "文件不符合规范!"
            data = '''{"message":"%s"}''' % format(message)
            return data

    if reqtype == 'HTTP'or 'XML':
        sql = selectrouteurl(routename)
        sqlite_connect = db_server.sqlite_connect()
        if sqlite_connect.selectrouteurl(sql) != False and reqtype == 'HTTP':
            reqtypehttp = '0'
            thekey = '-$$-'.join(thekey)
            thevalue = '-$$-'.join(thevalue)
            res = '-$$-'.join(res)
            insertsql = insertHttpWithLogicSql(reqtypehttp, routename, reponseMsg, thekey, thevalue, res)
            sqlite_connect.inserthttps(insertsql)
            sqlite_connect.closecon()
            message = "创建接口成功!"
            data = '''{"message":"%s"}''' % format(message)
            return data
        if sqlite_connect.selectrouteurl(sql) != False and reqtype == 'XML':
            reqtypexml = '2'
            insertsql = inserthttp(reqtypexml, routename, reponseMsg)
            sqlite_connect.inserthttps(insertsql)
            sqlite_connect.closecon()
            message = "创建接口成功!"
            data = '''{"message":"%s"}''' % format(message)
            return data
        else:
            message = "接口已存在!"
            data = '''{"message":"%s"}''' % format(message)
            return data
    else:
        message = "请输入正确的值!"
        data = '''{"message":"%s"}''' % format(message)
        return data