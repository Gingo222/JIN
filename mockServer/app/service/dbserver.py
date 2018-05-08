# -*- coding: utf-8 -*-
import MySQLdb
import json

class mysqlconnect():

    def __init__(self):
        con = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234qwer', db='flaskdb', charset='utf8')
        cursor = con.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.con = con
        self.cursor = cursor


    def inserthttps(self, sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception:
            self.con.rollback()
            return "执行sql失败"


    def selectrouteurl(self, sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
            data = self.cursor.fetchall()
            print "selectrouteurl返回信息:", data
            if len(data) >= 1:
                return False
        except Exception:
            self.con.rollback()
            return False


    def selmsg(self, sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
            data = self.cursor.fetchall()
        except Exception:
            self.con.rollback()
            return "异常,sql回滚"
        else:
            return data[0]['reponseMsg']

    # 用于删除与查询
    def selcer(self, sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
            data = self.cursor.fetchall()
        except Exception:
            self.con.rollback()
            return "异常,sql回滚"
        else:
            if not data:
                return "del"
            return data[0]

    def selAll(self, sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
            data = self.cursor.fetchall()
        except Exception:
            self.con.rollback()
            return "异常,sql回滚"
        else:
            jdata = json.dumps(data)
            return jdata


    def closecon(self):
        self.cursor.close()


    def closeconmysql(self):
        self.con.close()


