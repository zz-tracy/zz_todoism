# -*- coding: utf-8 -*-

"""
    :author: Dong Xiao (潇东)
    :url:
    :copyright:
    :license: MIT, see LICENSE for more details.

    : 用户接口
"""
from flask import render_template, request,Blueprint, jsonify
from flask_babel import _
from flask_login import current_user, login_required

from todoism.extensions import db
from todoism.models import SysUser

user_bp = Blueprint('user', __name__)
# print('----', __name__)
# print('----', '测试断点1')


# 注册新增用户路由
# 使用request.get_json()方法获取请求参数
@user_bp.route('/new', methods=['POST'])
@login_required
def new_user():
    # print('----', '测试断点2')
    data = request.get_json()
    print('----', data)
    if data['username'] is None or data['username'].strip() == '':
        return jsonify(message=_('Invalid user data.')), 400

    sys_user = SysUser(
        user_group_id=data['user_group_id'], username=data['username'], password=data['password'], salt=data['salt'],
        name=data['name'], phone=data['phone'], email=data['email'], creat_id=data['creat_id'],
        update_id=data['update_id'], last_login_time=data['last_login_time'], login_count=data['login_count']
    )

    db.session.add(sys_user)
    db.session.commit()
    return jsonify(code=200, message='ok', data=data)


# 使用request.form.get()方法获取请求参数
@user_bp.route('/new1', methods=['POST'])
@login_required
def new1_user():
    user_group_id = request.form.get('user_group_id')
    username = request.form.get('username')
    password = request.form.get('password')
    salt = request.form.get('salt')
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    creat_id = request.form.get('creat_id')
    update_id = request.form.get('update_id')
    last_login_time = request.form.get('last_login_time')
    login_count = request.form.get('login_count')

    sys_user = SysUser(
        user_group_id=user_group_id, username=username, password=password, salt=salt,
        name=name, phone=phone, email=email, creat_id=creat_id, update_id=update_id, last_login_time=last_login_time,
        login_count=login_count
    )
    db.session.add(sys_user)
    db.session.commit()
    # data = [
    # user_group_id, username, password, salt, name, phone, email, creat_id, update_id, last_login_time, login_count
    # ]
    data = {
        'user_group_id': user_group_id,
        'username': username,
        'password': password,
        'salt': salt,
        'name': name,
        'phone': phone,
        'email': email,
        'creat_id': creat_id,
        'update_id': update_id,
        'last_login_time': last_login_time,
        'login_count': login_count
    }
    return jsonify(code=200, message='ok', data=data)


# 注册编辑用户路由
# 使用request.get_json()方法获取参数
@user_bp.route('/user/<int:user_id>/edit', methods=['PUT'])
@login_required
def edit_user(user_id):
    user = SysUser.query.get(user_id)
    # if current_user != user.author:
    #     return jsonify(message=_('Permission denied.')), 403

    data = request.get_json()
    print('----', data)
    if data is None or data['name'].strip() == '':
        return jsonify(message=_('Invalid user name.')), 400
    user.name = data['name']
    db.session.commit()
    return jsonify(code=200, message='ok', data=data['name'])
    # return jsonify(message=_('SysUser updated.'))


# 使用request.form.get()方法获取参数
@user_bp.route('/user/<int:user_id>/edit1', methods=['PUT'])
@login_required
def edit1_user(user_id):
    user = SysUser.query.get(user_id)
    # print('----', user)
    # if current_user != user.author:
    #     return jsonify(message=_('Permission denied.')), 403

    name = request.form.get('name')
    print('----', name)
    if name is None or name.strip() == '':
        return jsonify(message=_('Invalid user name.')), 400
    user.name = name
    db.session.commit()
    return jsonify(code=200, message='ok', data=name)
    # return jsonify(message=_('SysUser updated.'))


# 注册查询路由
@user_bp.route('/user', methods=['POST'])
@login_required
def query_user():
    users = SysUser.query.all()
    data = []
    for user in users:
        item = {
            'user_group_id': user.id,
            'username': user.username,
            'password': user.password,
            'salt': user.salt,
            'name': user.name,
            'phone': user.phone,
            'email': user.email,
            'creat_id': user.creat_id,
            'update_id': user.update_id,
            'last_login_time': user.last_login_time,
            'login_count': user.login_count
        }
        data.append(item)
        # return jsonify(code=200, message='ok', data=data)
    # print('----', user)
    # data = user[:]
    # print(data)
    return jsonify(code=200, message='ok', data=data)


# 注册删除单个用户路由
@user_bp.route('/user/<int:user_id>/delete', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = SysUser.query.get(user_id)
    print('---', user)
    db.session.delete(user)
    db.session.commit()
    return jsonify(code=200, message='ok')


# 注册清空用户路由
@user_bp.route('/user/clear', methods=['DELETE'])
@login_required
def user_clear():
    users = SysUser.query.all()
    # print('----', users)
    # data = []
    for user in users:
        db.session.delete(user)
        # data.append(user)
    # print('----', data)
    # delete from SysUser
    # db.session.delete()
    db.session.commit()
    return jsonify(code=200, message='ok')

