# -*- coding: utf-8 -*-
# 插入https配置
def inserthttps(reqtype, routename, reponseMsg, keyword, keyid):
    sql = "INSERT INTO route (type, routeUrl, reponseMsg, httpskey, httpscerId) VALUES " \
          "('%s','%s','%s','%s','%s')" % (reqtype, routename, reponseMsg, keyword, keyid)
    return sql

# 插入http，xml
def inserthttp(reqtype, routename, reponseMsg):
    sql = "INSERT INTO route (type, routeUrl, reponseMsg) VALUES " \
          "('%s','%s','%s')" % (reqtype, routename, reponseMsg)
    return sql

#插入http，xml 包含逻辑
def insertHttpWithLogicSql(reqtype, routename, reponseMsg, thekey, thevalue, res):
    sql = "INSERT INTO route (type, routeUrl, reponseMsg,thekey, thevalue, res) VALUES " \
          "('%s','%s','%s','%s','%s','%s')" % (reqtype, routename, reponseMsg, thekey, thevalue, res)
    return sql

# 查询是否有重复路由
def selectrouteurl(routename):
    sql = "SELECT routeUrl FROM route WHERE routeUrl = '%s';" % routename
    return sql

# 查询返回信息
def selectrep(routename):
    sql = "SELECT reponseMsg FROM route WHERE routeUrl = '%s';" % routename
    return sql

# 查询逻辑返回res
def selectLogicRepSql(routename):
    sql = "SELECT res FROM route WHERE routeUrl = '%s';" % routename
    return sql

# 查询逻辑返回thekey
def selectLogicKeySql(routename):
    sql = "SELECT thekey FROM route WHERE routeUrl = '%s';" % routename
    return sql

# 查询逻辑返回thevalue
def selectLogicValueSql(routename):
    sql = "SELECT thevalue FROM route WHERE routeUrl = '%s';" % routename
    return sql

# 查询证书id, keyid
def selectcer(routename):
    sql = "SELECT httpscerId, httpskey FROM route WHERE routeUrl = '%s';" % routename
    return sql

# 插叙路由状态
def selecttype(routename):
    sql = "SELECT type FROM route WHERE routeUrl = '%s';" % routename
    return sql


# 10条每查
def selectAll(startNum):
    sql = "SELECT routeUrl, type, creater, DATE(createDate)as createDate FROM route ORDER BY id DESC LIMIT " + str(startNum) + ", 10;"
    return sql

def select_route_info(routename):
    sql = "SELECT routeUrl, type, creater, reponseMsg, DATE(createDate)as createDate, thekey, thevalue, res FROM route " \
          "WHERE routeUrl = " + "'" + routename + "';"
    return sql


#删除路由
def del_route(routename):
    sql = "DELETE FROM route WHERE routeUrl = '%s';" % routename
    return sql


#修改路由内容
def update_reponseMsg(routeName, theKey, theValue, res):
    sql = "UPDATE route set thekey = '%s', thevalue = '%s', res= '%s' WHERE routeUrl = '%s'" % (theKey, theValue, res, routeName)
    return sql

#统计数据量
def count_int():
    sql = "SELECT COUNT(routeUrl) as tolnub FROM route; "
    return sql

def tableExitsSql():
    sql = "CREATE TABLE IF NOT EXISTS `route`(`id` integer NOT NULL PRIMARY KEY AUTOINCREMENT," \
          "`routeUrl` varchar(200) NOT NULL," \
          "`k` text DEFAULT NULL ,  `v` text DEFAULT NULL ,  `r` TEXT DEFAULT NULL ,"\
          "`reponseMsg` text," \
          "`httpscerId` text," \
          "`httpskey` text," \
          "`type` varchar(2) NOT NULL DEFAULT '0'," \
          "`creater` varchar(100) DEFAULT 'tester'," \
          "`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP) ;"
    return sql
