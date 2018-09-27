# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors
import json
import ConfigParser


class MysqlConnect(object):
    configParser = ConfigParser.ConfigParser()
    configParser.read('../config/config.ini')

    def __init__(self):
        self.con = pymysql.connect(user=MysqlConnect.configParser.get('mysql', 'user'),
                                   password=MysqlConnect.configParser.get('mysql', 'password'),
                                   host=MysqlConnect.configParser.get('mysql', 'host'),
                                   port=int(MysqlConnect.configParser.get('mysql', 'port')),
                                   database=MysqlConnect.configParser.get('mysql', 'database'),
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
        self.cursor = self.con.cursor()

    def execute_select_status_sql(self, sql, kind):
        try:
            self.cursor.execute(sql)
            self.con.commit()
            result = self.cursor.fetchall()
            if kind == 'select_state' and len(result) == 1:
                return result[0]['state']
        except Exception as e:
            print(e)
            self.con.rollback()
            return False
        else:
            return result

    def execute_update_state_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
            result = self.cursor.fetchall()
        except Exception as e:
            print(e)
            self.con.rollback()
            return False
        else:
            return result
