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


# 查询是否有重复路由
def selectrouteurl(routename):
    sql = "SELECT routeUrl FROM route WHERE routeUrl = '%s';" % routename
    return sql


# 查询返回信息
def selectrep(routename):
    sql = "SELECT reponseMsg FROM route WHERE routeUrl = '%s';" % routename
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
    sql = "SELECT routeUrl, type, creater, date_format(createDate, '%Y-%m-%d')as createDate " \
          "FROM route ORDER BY id LIMIT " + str(startNum) + ", 10;"
    return sql

def select_route_info(routename):
    sql = "SELECT routeUrl, type, creater, reponseMsg, date_format(createDate, '%Y-%m-%d')as createDate FROM route " \
          "WHERE routeUrl = " + "'" + routename + "';"
    return sql


#删除路由
def del_route(routename):
    sql = "DELETE FROM route WHERE routeUrl = '%s';" % routename
    return sql


#修改路由内容
def update_reponseMsg(routeName, responseMsg):
    sql = "UPDATE route set reponseMsg = '%s' WHERE routeUrl = '%s'" % (responseMsg, routeName)
    return sql

#统计数据量
def count_int():
    sql = "SELECT COUNT(routeUrl) as tolnub FROM route; "
    return sql
