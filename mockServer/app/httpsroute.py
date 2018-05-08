# -*- coding: utf-8 -*-
from flask import Flask
import service.dbsqliteserver as db_server
import ConfigParser
from service.mockdbsql import selectrep


app = Flask(__name__)
cf = ConfigParser.ConfigParser()
cf.read('config/route.conf')
port = cf.getint("routePort", "XMLPort")
fileFolder = cf.get("crtFile", "httpsCrt")
keyFolder = cf.get("crtFile", "httpsKey")


@app.route('/mock/https/<name>', methods=["GET", "POST"])
def https_mock(name):
    sql = selectrep(name)
    sqlite_Connnect = db_server.sqlite_connect()
    data = sqlite_Connnect.selmsg(sql)
    if data:
        return data
    return "无此路由"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002, ssl_context=(fileFolder, keyFolder))
