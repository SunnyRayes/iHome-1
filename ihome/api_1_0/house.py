# -*- coding:utf-8 -*-
from datetime import datetime

from sqlalchemy import or_

from ihome import db, constants, redis_store
from ihome.models import Area, House, Facility, HouseImage, Order
from ihome.utils.common import login_required
from ihome.utils.image_storage import upload_image
from . import api
from flask import jsonify, request, g, current_app, session
from ihome.response_code import RET


@api.route('/houses', methods=['GET'])
def get_house_list():
    """获取搜索房屋列表"""

    # 获取参数
    aid = request.args.get('aid')
    sk = request.args.get('sk')
    page_no = request.args.get('p')
    sd = request.args.get('sd')
    ed = request.args.get('ed')

    start_date = ''
    end_date = ''
    # 校验参数
    try:
        if aid:
            aid = int(aid)
        if page_no:
            page_no = int(page_no)
        if sd:
            start_date = datetime.strptime(sd, '%Y-%m-%d')
        if ed:
            end_date = datetime.strptime(ed, '%Y-%m-%d')
    except Exception as e:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    house_query = House.query
    try:
        # 搜索对应城区
        if aid:
            house_query = house_query.filter(House.area_id == aid)

        # 对日期进行过滤
        orders = []
        if start_date and end_date:
            orders = Order.query.filter(Order.begin_date < end_date, Order.end_date > start_date).all()
        elif start_date:
            orders = Order.query.filter(or_(Order.begin_date >= start_date, Order.end_date <= start_date)).all()
        elif end_date:
            orders = Order.query.filter(or_(Order.begin_date >= end_date, Order.end_date <= end_date)).all()
        if orders:
            house_ids = [order.house_id for order in orders]
            current_app.logger.debug(house_ids)
            house_query = house_query.filter(House.id.notin_(house_ids))

        # 排序
        if sk == 'booking':
            house_query = house_query.order_by(House.order_count.desc())
        elif sk == 'price-inc':
            house_query = house_query.order_by(House.price)
        elif sk == 'price-des':
            house_query = house_query.order_by(House.price.desc())
        else:
            house_query = house_query.order_by(House.create_time.desc())
        house_page = house_query.paginate(page_no, constants.HOUSE_LIST_PAGE_CAPACITY, False)
        houses = house_page.items
        total_page = house_page.pages
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询房屋信息失败')
    houses_list = [house.to_basic_dict() for house in houses]
    datas = {
        'houses': houses_list,
        'total_page': total_page
    }
    return jsonify(errno=RET.OK, errmsg='OK', data=datas)


@api.route('/house/index', methods=['GET'])
def get_house_index():
    """获取首页轮播房源，即最新的5间"""
    try:
        houses = House.query.order_by(House.create_time.desc())
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='查询房源失败')
    house_list = [house.to_basic_dict() for house in houses]
    return jsonify(errno=RET.OK, errmsg='OK', house_list=house_list)


@api.route('/house/<house_id>', methods=['GET'])
def get_house_detail(house_id):
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询信息失败')
    if not house:
        return jsonify(errno=RET.PARAMERR, errmsg='没有该房屋')
    user_id = session.get('user_id', -1)
    house_detail = house.to_full_dict()
    return jsonify(errno=RET.OK, errmsg='OK', data=house_detail, user_id=user_id)


@api.route('/house/images', methods=['POST'])
@login_required
def set_house_image():
    # 获取参数
    house_id = request.form.get('house_id')
    if not house_id:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少房屋信息')
    try:
        img_data = request.files.get('house_image')
    except Exception as e:
        return jsonify(errno=RET.PARAMERR, errmsg='获取图片失败')
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询房屋信息失败')
    if not house:
        return jsonify(errno=RET.PARAMERR, errmsg='房屋不存在')
    try:
        key = upload_image(img_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传图片失败')
    house_image = HouseImage()
    house_image.house_id = house.id
    house_image.url = key
    if not house.index_image_url:
        house.index_image_url = key
    # 保存房屋信息
    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存图片信息失败')
    img_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg='OK', data={'img_url': img_url})


@api.route('/house', methods=['POST'])
@login_required
def post_house():
    # 获取参数
    response_dict = request.json
    title = response_dict.get('title')
    price = response_dict.get('price')
    address = response_dict.get('address')
    area_id = response_dict.get('area_id')
    room_count = response_dict.get('room_count')
    acreage = response_dict.get('acreage')
    unit = response_dict.get('unit')
    capacity = response_dict.get('capacity')
    beds = response_dict.get('beds')
    deposit = response_dict.get('deposit')
    min_days = response_dict.get('min_days')
    max_days = response_dict.get('max_days')
    facility = response_dict.get('facility')

    # 校验参数
    if not all(
            [title, price, address, area_id, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    try:
        price = float(price) * 100
        deposit = float(deposit) * 100
    except Exception as e:
        return jsonify(errno=RET.PARAMERR, errmsg='金额类型不正确')

    # 设置房屋
    house = House()
    house.user_id = g.user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    if facility:
        facilities = Facility.query.filter(Facility.id.in_(facility)).all()
        house.facilities = facilities
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存房屋信息失败')

    return jsonify(errno=RET.OK, errmsg='OK', data={'house_id': house.id})


@api.route('/areas', methods=['GET'])
def get_areas():
    """获取城区信息"""
    # 查询所有地区
    try:  # 从redis中获取
        areas_list = redis_store.get('Areas')
        return jsonify(errno=RET.OK, errmsg='OK', data=eval(areas_list))
    except Exception as e:
        current_app.logger.error(e)
    try:  # 从数据库中获取
        areas = Area.query.all()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='获取参数失败')

    areas_list = [area.to_dict() for area in areas]

    try:  # 保存到redis中
        redis_store.set('Areas', areas_list, constants.AREA_INFO_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)

    return jsonify(errno=RET.OK, errmsg='OK', data=areas_list)
