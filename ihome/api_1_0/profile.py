# -*- coding:utf-8 -*-
from flask import g, current_app, jsonify, request

from ihome import db, constants
from ihome.models import User
from ihome.response_code import RET, error_map
from ihome.utils.common import login_required
from ihome.utils.image_storage import upload_image
from . import api


@api.route('/users/auth', methods=['GET'])
@login_required
def get_auth():
    try:
        user = User().query.get(g.user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')
    real_name = user.real_name
    id_card = user.id_card

    return jsonify(errno=RET.OK, errmsg='OK', data={'real_name': real_name, 'id_card': id_card})


@api.route('/users/auth', methods=['POST'])
@login_required
def set_auth():
    # 获取参数
    request_dict = request.json
    real_name = request_dict.get('real_name')
    id_card = request_dict.get('id_card')

    # 验证有效性
    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少必要参数')

    # 查询用户
    try:
        user = User().query.get(g.user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')
    if (user.real_name is not None) & (user.id_card is not None):
        return jsonify(errno=RET.DATAEXIST, errmsg='该用户已实名认证')
    user.real_name = real_name
    user.id_card = id_card
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存用户信息失败')

    return jsonify(errno=RET.OK, errmsg='OK')


@api.route('/users/avatar', methods=['POST'])
@login_required
def set_user_image():
    """设置用户头像"""
    # 判断是否登录
    # 获取头像参数
    try:
        img_data = request.files.get('avatar')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='传入参数错误')
    # 校验参数合法性

    # 上传图片
    try:
        key = upload_image(img_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传用户头像失败')

    # 查询用户
    try:
        user = User().query.get(g.user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    # 给用户添加图片链接
    user.avatar_url = key

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存用户头像失败')

    # 响应结果
    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg='OK', data={'avatar_url': avatar_url})


@api.route('/users', methods=['PUT'])
@login_required
def set_user_name():
    # 获取用户名
    request_dict = request.json
    user_name = request_dict.get('user_name')
    if not user_name:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少必要参数')
    try:
        user = User.query.get(g.user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')
    user.name = user_name

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])


@api.route('/users', methods=['GET'])
@login_required
def get_user_profile():
    try:
        user = User.query.get(g.user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')
    response_dict = {
        'name': user.name,
        'avatar_url': constants.QINIU_DOMIN_PREFIX + user.avatar_url
    }
    return jsonify(errno=RET.OK, errmsg='OK', data=response_dict)
