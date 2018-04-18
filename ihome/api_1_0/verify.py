# -*- coding:utf-8 -*-
from flask import make_response, request, jsonify, abort

from ihome import redis_store
from ihome.response_code import RET, error_map
from . import api
from ihome.utils.captcha.captcha import captcha


@api.route('/img_code')
def get_verify_code():
    # 获取UUID
    uuid = request.args.get('uuid')
    new_uuid = request.args.get('new_uuid')

    if not new_uuid:
        abort(403)

    # 获取验证码信息
    name, text, image = captcha.generate_captcha()

    try:
        if uuid:
            # 删除之前的验证信息
            redis_store.delete('Img_code:%s' % uuid)
        redis_store.set('Img_code:%s' % new_uuid, text)
    except Exception as e:
        print(e)
        return jsonify({'errcode': RET.DATAERR, 'errmsg': error_map[RET.DATAERR]})

    response = make_response(image)

    response.headers['Content-Type'] = 'image/jpg'

    return response
