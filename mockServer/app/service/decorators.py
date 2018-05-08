# -*- coding: utf-8 -*-
from flask import request


def get_value():
    message = "未获取正确参数!"
    data = '''{"message":"%s"}''' % format(message)
    try:
        reqtype = request.form.get('reqtype')
        routename = request.form.get('routename')
        reponseMsg = request.form.get('reponseMsg')
    except:
        return data