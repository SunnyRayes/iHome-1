# -*-coding:utf-8-*-
from flask import session, jsonify, g
from werkzeug.routing import BaseConverter
from ihome.response_code import RET, error_map
from functools import wraps


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


# 定义登录验证
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify(errno=RET.SESSIONERR, errmsg=error_map[RET.SESSIONERR])
        else:
            g.user_id = user_id
            return func(*args, **kwargs)

    return wrapper
