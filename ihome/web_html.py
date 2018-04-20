# -*- coding:utf-8 -*-
from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf

html = Blueprint('html', __name__)


@html.route('/<re(r".*"):file_name>')
def get_html(file_name):
    # 主页
    if file_name == '':
        file_name = 'index.html'

    # 网页标题图标
    if file_name != 'favicon.ico':
        file_name = 'html/%s' % file_name

    response = make_response(current_app.send_static_file(file_name))
    csrf_token = generate_csrf()
    response.set_cookie('csrf_token', csrf_token)
    return response
