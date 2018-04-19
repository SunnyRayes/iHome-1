# -*- coding:utf-8 -*-
import json
import random

import re

from flask import make_response, request, jsonify, abort
from ihome import redis_store
from ihome.response_code import RET, error_map
from . import api
from ihome.utils.captcha.captcha import captcha
from ihome.utils.SendTemplateSMS import CCP

old_uuid = ''


@api.route('/img_code')
def get_verify_code():
    # 获取UUID
    uuid = request.args.get('uuid')

    if not uuid:
        abort(403)

    # 获取验证码信息
    name, text, image = captcha.generate_captcha()

    try:
        if old_uuid:
            # 删除之前的验证信息
            redis_store.delete('Img_code:%s' % old_uuid)
        redis_store.set('Img_code:%s' % uuid, text)
    except Exception as e:
        print(e)
        return jsonify({'errcode': RET.DATAERR, 'errmsg': error_map[RET.DATAERR]})
    global old_uuid
    old_uuid = uuid

    response = make_response(image)

    response.headers['Content-Type'] = 'image/jpg'
    print(text)

    return response


@api.route('/sms_code', methods=['POST'])
def send_sms_code():
    # 接受参数
    request_str = request.data
    request_dict = json.loads(request_str)
    mobile = request_dict.get('mobile')
    img_code_client = request_dict.get('img_code')
    uuid = request_dict.get('uuid')

    # 验证参数合法性
    if not all([mobile, img_code_client, uuid]):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    if not re.match(r'1[3-8]\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号码不合法')
    try:
        img_code_server = redis_store.get('Img_code:%s' % uuid)
    except Exception as e:
        print(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    if not img_code_server:
        return jsonify(errno=RET.DATAERR, errmsg='验证码不存在')
    if img_code_client.upper() != img_code_server.upper():
        return jsonify(errno=RET.PARAMERR, errmsg='验证码错误')
    # 发送短信验证码
    sms_code = '%06d' % random.randint(0, 999999)
    result = CCP().sendTemplateSMS('13421416120', [sms_code], '1')
    if result:
        return jsonify(errno=RET.THIRDERR, errmsg=error_map[RET.THIRDERR])
    # 保存到ｒｅｄｉｓ中
    try:
        redis_store.set('sms_code:%s' % mobile, sms_code)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    return jsonify(errno=RET.OK, errmsg='发送验证码成功')
