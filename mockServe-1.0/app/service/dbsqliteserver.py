# -*- coding: utf-8 -*-
import sqlite3
import json
import os
import platform
from mockdbsql import tableExitsSql


def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


class sqlite_connect(object):
    # 初始化系统内的sqlite环境变量使sqlite可用
    # 创建初始链接和游标
    def __init__(self):
        if "WINDOWS" in platform.platform().upper():
            find_Sqlite = os.environ.get("Path")
            if "sqlite" not in find_Sqlite:
                absPath = os.getcwd()
                appPath = absPath.split("app")[0]
                if find_Sqlite[-1] != ";":
                    sqlitePath = ";" + appPath + "app\sqlite;"
                    self.newPath = os.environ["Path"] + sqlitePath
                else:
                    sqlitePath = appPath + "app\sqlite;"
                    self.newPath = os.environ["Path"] + sqlitePath
        self.con = sqlite3.connect("mockdb.db", check_same_thread=False)
        self.con.row_factory = dict_factory
        self.cursor = self.con.cursor()
        self.cursor.execute(tableExitsSql())

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

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
            if data:
                return data[0]["reponseMsg"]
            return "无此路由或返回结果为空"

    def selcer(self, sql):
        # 用于删除与查询
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

    def execSqlLogic(self, sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
            data = self.cursor.fetchall()
            if data:
                return data
        except Exception:
            self.con.rollback()
            return "false"
        else:
            return "None"

    def closecon(self):
        self.cursor.close()

    def closeconmysql(self):
        self.con.close()

if __name__ == '__main__':
    sqlite_connect()
