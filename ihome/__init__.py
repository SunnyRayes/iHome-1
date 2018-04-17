# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import Config

app = Flask(__name__)
# 读取配置
app.config.from_object(Config)

# 实例化数据库
db = SQLAlchemy(app)

# 实例化redis
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 开启csrf方法
CSRFProtect(app)

# 开启Session
Session(app)
