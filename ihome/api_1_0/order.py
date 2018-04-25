# -*- coding:utf-8 -*-
from datetime import datetime

from ihome import db
from ihome.models import House, Order
from ihome.response_code import RET
from ihome.utils.common import login_required
from . import api
from flask import request, jsonify, current_app, g


@api.route('/orders', methods=['POST'])
@login_required
def add_order():
    """添加订单"""
    # 获取参数
    request_dict = request.json
    house_id = request_dict.get('house_id')
    sd = request_dict.get('sd')
    ed = request_dict.get('ed')

    # 校验参数
    if not all([house_id, sd, ed]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少必要参数')

    try:
        start_date = datetime.strptime(sd, '%Y-%m-%d')
        end_date = datetime.strptime(ed, '%Y-%m-%d')
        assert start_date < end_date, Exception('参数错误')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        house = House.query.filter(House.id == house_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')
    if not house:
        return jsonify(errno=RET.PARAMERR, errmsg='房屋不存在')

    # 查询订单是否冲突
    try:
        conflict_orders = Order.query.filter(start_date < Order.begin_date, Order.end_date < end_date,
                                             Order.house_id == house_id).all()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')
    if conflict_orders:
        return jsonify(errno=RET.PARAMERR, errmsg='预定日期冲突')

    # 保存订单
    order = Order()
    order.user_id = g.user_id  # 下订单的用户编号
    order.house_id = house.id  # 预订的房间编号
    order.begin_date = start_date  # 预订的起始时间
    order.end_date = end_date  # 预订的结束时间
    order.days = (end_date - start_date).days  # 预订的总天数
    order.house_price = house.price  # 房屋的单价
    order.amount = order.days * house.price  # 订单的总金额
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
    return jsonify(errno=RET.OK, errmsg='OK')
