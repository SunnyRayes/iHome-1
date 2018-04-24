# -*-coding:utf-8 -*-
import re
from flask import request, jsonify, current_app, session

from ihome import redis_store, db
from ihome.models import User
from ihome.response_code import RET, error_map
from ihome.utils.common import login_required
from . import api


@api.route('/sessions', methods=['GET'])
def check_login():
    name = session.get('name')
    user_id = session.get('user_id')
    if not name:
        return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    return jsonify(errno=RET.OK, errmsg='OK', data={'name': name, 'user_id': user_id})


@api.route('/sessions', methods=['DELETE'])
@login_required
def logout():
    """退出登录"""
    session.pop('name')
    session.pop('mobile')
    session.pop('user_id')
    return jsonify(errno=RET.OK, errmsg='OK')


@api.route('/sessions', methods=['POST'])
def login():
    # 获取参数
    request_dict = request.json
    mobile = request_dict.get('mobile')
    password = request_dict.get('password')

    # 判断有效性
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
    if not re.match(r'^1[3-8]\d{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号不合法')

    # 查询数据库
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')
    if user is None:
        return jsonify(errno=RET.PARAMERR, errmsg='用户或密码错误')
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='用户名或密码错误')

    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile
    return jsonify(errno=RET.OK, errmsg='登录成功')


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

    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile
    return jsonify(errno=RET.OK, errmsg='注册成功')
