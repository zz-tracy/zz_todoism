# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.

    :认证蓝本
"""
from faker import Faker
from flask import render_template, redirect, url_for, Blueprint, request, jsonify
from flask_babel import _
from flask_login import login_user, logout_user, login_required, current_user

from todoism.extensions import db
from todoism.models import User, Item

#从Flask导入Blueprint类，实例化这个类就获得了我们的蓝本对象。构造方法中的第一个参数是蓝本的名称；
# 第二个参数是包或模块的名称，我们可以使用__name__变量.
auth_bp = Blueprint('auth', __name__)

# 实例化Faker类,用于生成虚拟数据
fake = Faker()


# 使用auth_bp蓝本的route装饰器,注册登录路由
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    print('----', 'aaaa')
    # 判断当前用户是否是登录用户
    if current_user.is_authenticated:
    # redirect()函数为重定向函数,url_for()函数获取URL,其中第一参数为端点,该端点名为todo.app,用来标记视图函数以及对应的URL规则
        return redirect(url_for('todo.app'))
    # 判断请求方法是否是POST请求
    if request.method == 'POST':
        print('-----')
        data = request.get_json()    # 使用get_json()方法获取请求参数的字典,将返回的字典存储到data变量中
        # print('----', 'bbbb')
        username = data['username']    # 通过data['username']获取data字典中'username'对应的值
        password = data['password']    # 获取data字典中'password'对应的值
        # 通过User模型类的query属性查询,以及fileter_by()过滤方法和first()方法返回查询记录中的第一个记录
        user = User.query.filter_by(username=username).first()
        print(user)

        if user is not None and user.validate_password(password):
            # print('aaaa')
            # 调用login_user函数,并把user(实际的用户对象)以参数的形式传递给该函数,
            # 该函数返回True时,则进行登录,返回False,将不会登录
            login_user(user)
            return jsonify(message=_('Login success.'))     # 返回JSON格式的登录成功的提示消息
        return jsonify(message=_('Invalid username or password.')), 400 # 返回JSON格式的消息提示(无效的用户名或密码),400状态码
    return render_template('_login.html')    # 返回渲染后的html登录页面

# 注册登出路由
@auth_bp.route('/logout')
@login_required    # 确保当前用户在调用实际视图函数之前是登录状态以及通过了身份验证
def logout():
    # if request.method == 'POST':
    #     print('aaa')
    #     return jsonify(message=_('退出成功'))
    # print('bbb')
    logout_user()    # 调用logout_user()函数,注销用户
    return jsonify(message=_('Logout success.'))    # 返回JSON格式的登出成功的消息提示


# 注册注册路由
@auth_bp.route('/register')
def register():
    # generate a random account for demo use
    username = fake.user_name()    # 调用fake实例的user_name()方法,生成一个虚拟用户名
    # make sure the generated username was not in database(确保生成的用户名不在数据库中)
    while User.query.filter_by(username=username).first() is not None:
        username = fake.user_name()
    password = fake.word()    # 生成一个虚拟的用户密码
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    # 添加几个待办条目作为示例
    item = Item(body=_('Witness something truly majestic'), author=user)
    item2 = Item(body=_('Help a complete stranger'), author=user)
    item3 = Item(body=_('Drive a motorcycle on the Great Wall of China'), author=user)
    item4 = Item(body=_('Sit on the Great Egyptian Pyramids'), done=True, author=user)    # done=true 标记为完成状态
    db.session.add_all([item, item2, item3, item4])
    db.session.commit()
    # 使用jsonify()函数返回JSON格式的用户名、密码和提示消息。
    return jsonify(username=username, password=password, message=_('Generate success.'))
