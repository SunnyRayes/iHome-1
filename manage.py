# -*-coding:utf-8-*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:fuckyou@127.0.0.1:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
# 读取配置
app.config.from_object(Config)

# 实例化数据库
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run()
