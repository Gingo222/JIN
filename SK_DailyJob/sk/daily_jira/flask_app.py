import inject
from flask import Flask, g, request
from flask_compress import Compress
from daily_jira.resource import (efficient, jira)


def create_app():
    app = Flask(__name__)
    Compress(app)

    # 注册路由表
    blueprints = (
        efficient.get_resources(),
        jira.get_resources()
    )
    for bp in blueprints:
        app.register_blueprint(bp)
    app.url_map.strict_slashes = False

    return app
