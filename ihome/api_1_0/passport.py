# -*-coding:utf-8 -*-
import re
from flask import request, jsonify

from ihome import redis_store, db
from ihome.models import User
from ihome.response_code import RET, error_map
from . import api


@api.route('/users', methods=['POST'])
def register():
    # 获取参数
    request_dict = request.json
    mobile = request_dict.get('mobile')
    sms_code_client = request_dict.get('sms_code')
    password = request_dict.get('password')
    password2 = request_dict.get('password2')
    # 判断参数有效性
    if not all([mobile, sms_code_client, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    if not re.match(r'^1[3-8]\d{9}$', mobile):
        return jsonify(errom=RET.PARAMERR, errmsg='手机号码格式不合法')
    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg='两次输入的密码不一致')
    try:
        sms_code_server = redis_store.get('sms_code:%s' % mobile)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    if not sms_code_server:
        return jsonify(errno=RET.DATAERR, errmsg='验证码不存在，请先获取验证码')
    if sms_code_client != sms_code_server:
        return jsonify(errno=RET.PARAMERR, errmsg='手机验证码错误')
    user = User()
    user.mobile = mobile
    user.name = mobile
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify(errno=RET.OK, errmsg='注册成功')
