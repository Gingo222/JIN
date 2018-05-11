# -*- coding: utf-8 -*-
from sig import Sig_Server as e
from flask import Flask

app = Flask(__name__)

@app.route("/req/<name>", methods="POST")
def sig_controll(name):
    if name.upper() not in e:
        return "加密类型暂时不支持"


