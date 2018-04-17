# -*- coding:utf-8 -*-
import redis


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


class DevelopmentConfig(Config):
    """开发环境"""
    pass


class ProductConfig(Config):
    """生产环境"""
    DUBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:fuckyou@127.0.0.1:3306/db_ihome'


class UnittestConfig(Config):
    """测试环境"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:fuckyou@127.0.0.1:3306/ihome_test'


# 用字典存储配置类
configs = {
    'development': DevelopmentConfig,
    'product': ProductConfig,
    'unittest': UnittestConfig
}
