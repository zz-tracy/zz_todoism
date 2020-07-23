# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.

    : 主页蓝本
"""
from flask import render_template, Blueprint, current_app, make_response, jsonify
from flask_babel import _
from flask_login import current_user

from todoism.extensions import db

# 实例化主页蓝本,并传入'home'蓝本名,以及todoism.blueprints.home包/模块的名称
home_bp = Blueprint('home', __name__)
# print('----', __name__)

# 注册主页的路由
@home_bp.route('/')
def index():
    return render_template('index.html')    # 返回html格式的主页页面


# 注册介绍路由
@home_bp.route('/intro')
def intro():
    return render_template('_intro.html')    # 返回html格式的介绍页面

# 设置区域的路由
@home_bp.route('/set-locale/<locale>')
def set_locale(locale):
    if locale not in current_app.config['TODOISM_LOCALES']:    # 通过if语句判断locale(区域代码)是否在当前程序下的设置的'TODOISM_LOCALES'列表中
        return jsonify(message=_('Invalid locale.')), 404    # 如果不在则返回JSON格式的错误消息提示, 错误状态码为404

    # 调用make_response()函数将JSON格式的提示消息存储在response变量中
    response = make_response(jsonify(message=_('Setting updated.')))
    # 判断当前用户是否是已登录用户
    if current_user.is_authenticated:
        print('----', '测试断点7')
        current_user.locale = locale    # 把当前登录用户的区域代码存储到User数据库模型的local字段中
        db.session.commit()    # 将登陆用户区域代码提交到数据库中
    else:
    # 如果是匿名用户,则通过对response变量调用set_cookie()函数获取区域代码,其中函数的第一个参数为区域代码名,第二个参数为区域代码,
    # 第三个参数是改区域代码在cookie中保留的最长时间(以第一次被请求的时间开始计算)
        response.set_cookie('locale', locale, max_age=60 * 60 * 24 * 30)
    return response
