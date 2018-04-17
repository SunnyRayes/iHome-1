# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import configs

# 实例化数据库
db = SQLAlchemy()

# 实例化redis
redis_store = None

# 开启csrf方法
csrf = CSRFProtect()


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
    Session(app)
    return app
