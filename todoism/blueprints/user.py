# -*- coding: utf-8 -*-

"""
    :author: Dong Xiao (潇东)
    :url:
    :copyright:
    :license: MIT, see LICENSE for more details.

    : 用户接口
"""
from flask import render_template, request, Blueprint, jsonify
from flask_babel import _
from flask_login import current_user, login_required
from sqlalchemy import and_
from sqlalchemy import or_

from todoism.extensions import db
from todoism.models import SysUser

user_bp = Blueprint('user', __name__)


# print('----', __name__)
# print('----', '测试断点1')


# 注册新增用户路由
# 使用request.get_json()方法获取请求参数
@user_bp.route('/new1', methods=['POST'])
@login_required
def new_user():
    # print('----', '测试断点2')
    data = request.get_json()
    # print('----', data)
    if data['username'] is None or data['username'].strip() == '':
        return jsonify(message=_('Invalid user data.')), 400

    #  通过filter()过滤方法查询username字段对应的记录
    # username = SysUser.query.filter(SysUser.username == data['username']).first()
    # 通过filter_by过滤方法查询username对应的记录
    username = SysUser.query.filter_by(username=data['username']).first()

    # print('----', username)
    # if username is not None:
    #     return jsonify(message=_('The user name already exists.')), 404

    sys_user = SysUser(
        gender=data['gender'], age=data['age'], user_group_id=data['user_group_id'], username=data['username'],
        password=data['password'], salt=data['salt'], name=data['name'], phone=data['phone'], email=data['email'],
        creat_id=data['creat_id'], update_id=data['update_id'], last_login_time=data['last_login_time'],
        login_count=data['login_count']
    )
    db.session.add(sys_user)
    db.session.commit()
    return jsonify(code=200, message='ok', data=data)


# 使用request.form.get()方法获取请求参数
@user_bp.route('/new2', methods=['POST'])
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

    username = SysUser.query.filter_by(username=username).first()
    # print('----', username)
    if username is not None:
        return jsonify('The user name already exists.'), 404

    sys_user = SysUser(
        user_group_id=user_group_id, username=username, password=password, salt=salt,
        name=name, phone=phone, email=email, creat_id=creat_id, update_id=update_id, last_login_time=last_login_time,
        login_count=login_count
    )
    db.session.add(sys_user)
    db.session.commit()
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


# 注册编辑用户动态路由
# 使用request.get_json()方法获取参数
# 通过url获取id
@user_bp.route('/user/<int:user_id>/edit1', methods=['PUT'])
@login_required
def edit1_user(user_id):
    user = SysUser.query.get(user_id)
    # if current_user != user.author:
    #     return jsonify(message=_('Permission denied.')), 403

    if user is None:
        return jsonify(message=_('Invalid user id.')), 404

    data = request.get_json()
    # print('----', data)
    if data is None or data['name'].strip() == '':
        return jsonify(message=_('Invalid user name.')), 400

    # 通过len()方法对用户输入的name值的字符长度的最大值及最小值进行判断
    if 10 > len(data['name']) > 64:
        return jsonify(message=_('The user name is too long.')), 401

    user.name = data['name']
    db.session.commit()
    return jsonify(code=200, message='ok', data=data['name'])


# 注册编辑用户静态路由
# 使用request.get_json()方法获取参数
# 使用get_json()方法获取id
@user_bp.route('/user/edit1', methods=['PUT'])
@login_required
def edit2_user():
    # if current_user != user.author:
    #     return jsonify(message=_('Permission denied.')), 403

    data = request.get_json()
    # print('----', data)
    if data is None \
            or data['name'].strip() == '' \
            or 10 > len(data['name']) > 64:
        return jsonify(message=_('Invalid user name.')), 400

    user = SysUser.query.get(data['id'])
    if user is None:
        return jsonify(message=_('Invalid user id.')), 404
    user.name = data['name']
    db.session.commit()
    return jsonify(code=200, message='ok', data=data)


# 使用request.form.get()方法获取参数
# 通过url获取id
@user_bp.route('/user/<int:user_id>/edit2', methods=['PUT'])
@login_required
def edit3_user(user_id):
    user = SysUser.query.get(user_id)
    # print('----', user)
    # if current_user != user.author:
    #     return jsonify(message=_('Permission denied.')), 403

    if user is None:
        return jsonify(message='Invalid user id.'), 404

    name = request.form.get('name')
    # print('----', name)
    if name is None \
            or name.strip() == '' \
            or 10 > len(name) > 64:
        return jsonify(message=_('Invalid user name.')), 400

    user.name = name
    db.session.commit()
    return jsonify(code=200, message='ok', data=name)


# 通过request.form.get()获取id
@user_bp.route('/user/edit2', methods=['PUT'])
@login_required
def edit4_user():
    name = request.form.get('name')
    user_id = request.form.get('id')
    # print('----',  name)
    # print('----', id)
    if name is None \
            or name.strip() == '' \
            or 10 > len(name) > 64:
        return jsonify(message=_('Invalid user name.')), 400

    user = SysUser.query.get(user_id)
    if user is None:
        return jsonify(message=_('Invalid user id.')), 404

    user.name = name
    db.session.commit()
    return jsonify(code=200, message='ok', data=name)


# 注册查询路由
@user_bp.route('/user1', methods=['POST'])
@login_required
def query_user1():
    users = SysUser.query.all()
    data = []
    for user in users:
        item1 = {
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
        data.append(item1)
    return jsonify(code=200, message='ok', data=data)


# # 使用filter()方法注册查询路由
# @user_bp.route('/user2', methods=['POST'])
# @login_required
# def query_user2():
#     # data = request.get_json()
#     # print('----', data)
#     # print('----', data['name'])
#     # if data is None \
#     #         or data['name'].strip() == '':
#     #     return jsonify(message=_('Invalid data.')), 400
#
#     # 使用filter()过滤方法及"=="查询操作符进行查询
#     # users = SysUser.query.filter(SysUser.name == data['name']).first()
#     # # print('----', users)
#     # if users is None:
#     #     return jsonify(message=_('Invalid users.')), 404
#
#     # 使用filter()过滤方法及'!='查询操作符进行查询
#     # users = SysUser.query.filter(SysUser.name != data['name']).first()
#     # if users is None:
#     #     return jsonify(message=_('Invalid users.')), 404
#
#     # 使用filter()过滤方法及'like(区分大小写, 模糊查询)'查询操作符进行查询
#     hello = request.get_json()['hello']
#     users = SysUser.query.filter(SysUser.username.like('%' + hello + '%')).all()
#     print('----', users)
#     if users is None:
#         return jsonify(message=_('Invalid users.')), 404
#
#     # 使用filter()过滤方法及'ilike(不区分大小写)'
#     users = SysUser.query.filter(SysUser.username.ilike('%Hello%')).all()
#     print('----', users)
#     if users is None:
#         return jsonify(message=_('Invalid users.')), 404
#
#     # 使用filter()过滤方法及'in'查询操作符进行查询
#     # users = SysUser.query.filter(SysUser.name.in_(data['names'])).all()
#     # print('----', users)
#     # if users is None:
#     #     return jsonify(message=_('Invalid users.')), 404
#
#     # 使用filter()过滤方法及'not in'查询操作符进行查询
#     # users = SysUser.query.filter(SysUser.name.notin_(data['names'])).all()
#     # if users is None:
#     #     return jsonify(message=_('Invalid users.')), 404
#
#     # 使用and_()
#     # users = SysUser.query.filter(and_(SysUser.name == data['name'], SysUser.username == data['username'])).all()
#     # if users is None:
#     #     return jsonify(message=_('Invalid users.')), 404
#
#     # 在filter()中加入多个表达式,使用逗号分隔,表示表示同时满足两个表达式的数据
#     # users = SysUser.query.filter(SysUser.name == data['name'], SysUser.username == data['username']).all()
#     # if users is None:
#     #     return jsonify(message=_('Invalid users.')), 404
#
#     # 在filter()方法中叠加调用多个filter()方法
#     # users = SysUser.query.filter(SysUser.name == data['name']).filter(SysUser.username == data['username']).all()
#     # if users is None:
#     #     return jsonify(message=_('Invalid users.')), 404
#
#     # 在filter()方法中使用or_()
#     # users = SysUser.query.filter(or_(SysUser.name == data['name'], SysUser.username == data['username'])).all()
#     # # print('----', users)
#     # if users is None:
#     #     return jsonify(message=_('Invalid users.')), 404
#
#     # 使用order_by()方法进行单字段正排序
#     users = SysUser.query.order_by('age').all()
#     # print('----', users)
#     if users is None:
#         return jsonify(message=_('Invalid users.')), 404
#
#     # 使用order_by()方法进行单字段倒排序
#     # users = SysUser.query.order_by(SysUser.age.desc()).all()
#     # # print('----', users)
#     # if users is None:
#     #     return jsonify(message=_('Invalid users.')), 404
#
#     # 通过db.session使用order_by()方法进行多字段正排序
#     users = db.session.query(SysUser.age, SysUser.name, SysUser.username).order_by('age').all()
#     # print('----', users)
#     if users is None:
#         return jsonify(message=_('Invalid users.')), 404
#
#     # 通过db.session使用order_by()方法进行多字段倒排序
#     users = db.session.query(SysUser.age, SysUser.name, SysUser.username).order_by(SysUser.age.desc()).all()
#     # print('----', users)
#     if users is None:
#         return jsonify(message=_('Invalid users.')), 404
#
#     # items = []
#     # for user in users:
#     #     item2 = {
#     #         "gender": user.gender,
#     #         'age': user.age,
#     #         'user_group_id': user.id,
#     #         'username': user.username,
#     #         'password': user.password,
#     #         'salt': user.salt,
#     #         'name': user.name,
#     #         'phone': user.phone,
#     #         'email': user.email,
#     #         'creat_id': user.creat_id,
#     #         'update_id': user.update_id,
#     #         'last_login_time': user.last_login_time,
#     #         'login_count': user.login_count
#     #     }
#     #     items.append(item2)
#     # item2 = {
#     #         'gender': users.gender,
#     #         'user_group_id': users.id,
#     #         'username': users.username,
#     #         'password': users.password,
#     #         'salt': users.salt,
#     #         'name': users.name,
#     #         'phone': users.phone,
#     #         'email': users.email,
#     #         'creat_id': users.creat_id,
#     #         'update_id': users.update_id,
#     #         'last_login_time': users.last_login_time,
#     #         'login_count': users.login_count
#     #     }
#     return jsonify(code=200, message='ok', data=users)
#
#
# # 查询----使用paginate()方法实现分页功能
# @user_bp.route('/user3', methods=['POST'])
# @login_required
# def query_user3():
#     data = request.get_json()
#     # 一页多少条:page_size, 当前第几页: page
#     page = data['page']
#     page_size = data['page_size']
#     users = db.session.query(SysUser.age, SysUser.name, SysUser.username)\
#         .order_by(SysUser.age.desc()).paginate(page, page_size)
#     print('----', db.session.query(SysUser.age, SysUser.name, SysUser.username).order_by(SysUser.age.desc()))
#     print('---', users.items)
#     items = users.items
#     if users is None:
#         return jsonify(message=_('Invalid users.')), 404
#
#     return jsonify(code=200, message='ok', data=items)


# 注册删除单个用户路由
@user_bp.route('/user/<int:user_id>/delete1', methods=['DELETE'])
@login_required
def delete_user1(user_id):
    user = SysUser.query.get(user_id)
    # print('---', user)
    db.session.delete(user)
    db.session.commit()
    return jsonify(code=200, message='ok')


# 使用request.get_json()方法获取id
# 注册删除单个用户路由
@user_bp.route('/user/delete2', methods=['DELETE'])
@login_required
def delete_user2():
    user_id = request.get_json()
    # print('----', user_id)
    if user_id is None:
        return jsonify(message=_('Invalid user id.')), 400

    user = SysUser.query.get(user_id['id'])
    # print('----', user)
    db.session.delete(user)
    db.session.commit()
    return jsonify(code=200, message='ok')


# 使用request.form.get()方法获取id
# 注册删除单个用户路由
@user_bp.route('/user/delete3', methods=['DELETE'])
def user_delete3():
    user_id = request.form.get('id')
    if user_id is None:
        return jsonify(message=_('Invalid user id.')), 400

    user = SysUser.query.get(user_id)
    if user is None:
        return jsonify(message=_('Invalid user id.')), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify(code=200, message='ok')


# 注册清空用户路由
# 使用for循环逐个删除
@user_bp.route('/user/clear1', methods=['DELETE'])
@login_required
def user_clear1():
    users = SysUser.query.all()
    # print('----', users)
    for user in users:
        db.session.delete(user)
    db.session.delete()
    db.session.commit()
    return jsonify(code=200, message='ok')


# 注册根据ids参数传递的id值进行批量删除
@user_bp.route('/user/clear2', methods=['DELETE'])
@login_required
def user_clear2():
    # 通过id列表删除指定id的条目
    data = request.get_json()
    ids = data['ids']
    if data is None or data['ids'] == '':
        return jsonify(meeage=_('Invalid data.')), 400

    for item in ids:
        user = SysUser.query.filter_by(id=item).first()
        db.session.delete(user)

    db.session.commit()
    return jsonify(code=200, message='ok')


# 注册批量清空路由
@user_bp.route('/user/clear3', methods=['DELETE'])
@login_required
def user_clear3():
    SysUser.query.delete()
    db.session.commit()
    return jsonify(code=200, message='ok')
