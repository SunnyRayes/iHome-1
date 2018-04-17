# -*-coding:utf-8-*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:fuckyou@127.0.0.1:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run()
