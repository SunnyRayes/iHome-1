# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import configs
from utils.common import RegexConverter

# 实例化数据库
db = SQLAlchemy()

# 实例化redis
redis_store = None

# 开启csrf方法
csrf = CSRFProtect()

# session
session = Session()


def create_app(config_name):
    app = Flask(__name__)
    # 读取配置
    app.config.from_object(configs[config_name])

    # 实例化数据库
    db.init_app(app)

    # 实例化redis
    global redis_store
    redis_store = redis.StrictRedis(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT)

    # 开启csrf方法
    csrf.init_app(app)

    # 开启Session
    session.init_app(app)

    # 注册自定义转换器
    app.url_map.converters['re'] = RegexConverter

    # 注册蓝图
    from ihome.api_1_0 import api
    app.register_blueprint(api)

    # 注册静态html界面蓝图
    from web_html import html
    app.register_blueprint(html)

    return app
