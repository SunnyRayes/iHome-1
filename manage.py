# -*-coding:utf-8-*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session


class Config(object):
    DEBUG = True
    SECRET_KEY = 'fsadlkfqwioeruyioity8we2q43/2kjH*&#@$b987493w8b9q87b392873'

    # mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:fuckyou@127.0.0.1:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 86400  # session 的有效期，单位是秒


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


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run()
