# -*- coding:utf-8 -*-
from datetime import datetime

from ihome import db
from ihome.models import House, Order
from ihome.response_code import RET
from ihome.utils.common import login_required
from . import api
from flask import request, jsonify, current_app, g


@api.route('/order/comment/<order_id>', methods=['POST'])
@login_required
def set_order_comment(order_id):
    comment = request.json.get('comment')
    if not comment:
        return jsonify(errno=RET.PARAMERR, errmsg='请填写评价')
    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == g.user_id,
                                   Order.status == 'WAIT_COMMENT').first()
        house = order.house
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    house.order_count += 1
    order.status = 'COMPLETE'
    order.comment = comment
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
    return jsonify(errno=RET.OK, errmsg='OK')


@api.route('/order/status/<order_id>', methods=['PUT'])
@login_required
def handle_orders(order_id):
    action = request.args.get('action')
    if action not in ['accept', 'reject']:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    try:
        houses = House.query.filter(House.user_id == g.user_id)
        houses_id = [house.id for house in houses]
        order = Order.query.filter(Order.id == order_id, Order.house_id.in_(houses_id),
                                   Order.status == 'WAIT_ACCEPT').first()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')
    if not order:
        return jsonify(errno=RET.PARAMERR, errmsg='订单不存在')
    if action == 'accept':
        order.status = 'WAIT_COMMENT'
    else:
        reject_reason = request.json.get('reject_reason')
        if not reject_reason:
            return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
        order.status = 'REJECTED'
        order.comment = reject_reason
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
    return jsonify(errno=RET.OK, errmsg='OK')


@api.route('/order', methods=['GET'])
@login_required
def get_orders():
    """获取用户订单"""
    role = request.args.get('role')
    if role not in ['customer', 'landlord']:
        return jsonify(errno=RET.PARAMERR, errmsg='参数不正确')
    orders = []
    try:
        if role == 'customer':
            orders = Order.query.filter(Order.user_id == g.user_id).all()
        else:
            houses = House.query.filter(House.user_id == g.user_id).all()
            house_ids = [house.id for house in houses]
            orders = Order.query.filter(Order.house_id.in_(house_ids)).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')
    orders_info = [order.to_dict() for order in orders]
    return jsonify(errno=RET.OK, errmsg='OK', data=orders_info)


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
