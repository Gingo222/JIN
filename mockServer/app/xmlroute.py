# -*- coding: utf-8 -*-
import logging
import ConfigParser
import service.dbsqliteserver as db_server
from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from service.mockdbsql import selectrep, selecttype

cf = ConfigParser.ConfigParser()
cf.read('config/route.conf')
port = cf.getint("routePort", "XMLPort")

class HelloWorldService(ServiceBase):
    # yon
    logging.basicConfig(level=logging.DEBUG)
    @rpc(String, _returns=String)
    def hello(ctx, name):
        try:
            with open("aa.xml", "r+") as filexml:
                source = filexml.read()
                print(name)
                return source.decode('utf-8')
        except Exception as e:
            print(e)
            return "error"

    @rpc(String, _returns=String)
    def helloGingo(ctx, routename):
        sqlite_Connect = db_server.sqlite_connect()
        sqlxml = selecttype(routename)
        sql = selectrep(routename)
        # 判断是否是xml类型
        reqtype = sqlite_Connect.selcer(sqlxml)
        if reqtype["type"] != '2':
            return u"此接口不为xml类型"
        reponseMsg = sqlite_Connect.selmsg(sql)
        if reponseMsg != False:
            return reponseMsg
        return u"无此路由"

application = Application([HelloWorldService],
    tns='helloGingo',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
    )


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', port, wsgi_app)
    server.serve_forever()
