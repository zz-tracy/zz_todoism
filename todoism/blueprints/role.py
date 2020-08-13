# -*- coding: utf-8 -*-
"""
    :author: Dong Xiao (潇东)
    :url:
    :copyright:
    :license: MIT, see LICENSE for more details.

    :角色接口
"""
from flask import Blueprint, request, jsonify
from flask_babel import _
from flask_login import login_required

from todoism.extensions import db
from todoism.models import Role

role_bp = Blueprint('role', __name__)
# print('----', __name__)


# 注册增加角色路由
@role_bp.route('/role/new1', methods=['POST'])
@login_required
def role_new1():
    # 使用get_json()方法获取请求参数
    data = request.get_json()
    if data is None:
        return jsonify(message=_('Invalid data.')), 400

    role = Role(
        name=data['name'],
        creat_time=data['creat_time'],
        update_time=data['update_time'],
        creat_id=data['creat_id'],
        update_id=data['update_id']
    )
    db.session.add(role)
    db.session.commit()
    return jsonify(code=200, message='ok', data=data)


# 注册新增角色路由
@role_bp.route('/role/new2', methods=['POST'])
@login_required
def role_new2():
    name = request.form.get('name')
    creat_time = request.form.get('creat_time')
    update_time = request.form.get('update_time')
    creat_id = request.form.get('creat_id')
    update_id = request.form.get('update_id')
    items = [name, creat_time, update_time, creat_id, update_id]
    for data in items:
        if data is None:
            return jsonify(message=_('Invalid data.')), 400

    role = Role(
        name=name,
        creat_time=creat_time,
        update_time=update_time,
        creat_id=creat_id,
        update_id=update_id
    )
    db.session.add(role)
    db.session.commit()
    roles = {
        'name': name,
        'creat_time': creat_time,
        'update_time': update_time,
        'creat_id': creat_id,
        'update_id': update_id
    }
    return jsonify(code=200, message='ok',  data=roles)


# 注册修改角色路由
# 通过URL获取id
@role_bp.route('/role/<int:role_id>/modify1', methods=['PUT'])
@login_required
def role_modify1(role_id):
    role = Role.query.get(role_id)
    if role is None:
        return jsonify(message=_('Invalid role_id.')), 404
    # 通过get_json()方法获取请求参数
    data = request.get_json()
    if data is None:
        return jsonify(message=_('Invalid data.')), 400

    role.name = data['name']
    role.creat_time = data['creat_time']
    role.update_time = data['update_time']
    role.creat_id = data['creat_id']
    role.update_id = data['update_id']
    db.session.commit()
    return jsonify(code=200, message='ok', data=data)


# 注册修改角色路由
# 通过URL获取id
@role_bp.route('/role/<int:role_id>/modify2', methods=['PUT'])
@login_required
def role_modify2(role_id):
    role = Role.query.get(role_id)
    if role is None:
        return jsonify(message=_('Invalid role_id.')), 404

    # 使用form.get()方法获取请求参数
    name = request.form.get('name')
    creat_time = request.form.get('creat_time')
    update_time = request.form.get('update_time')
    creat_id = request.form.get('creat_id')
    update_id = request.form.get('update_id')
    items = [name, creat_time, update_time, creat_id, update_id]
    for data in items:
        if data is None:
            return jsonify(message=_('Invalid data.')), 400

    role.name = name
    role.creat_time = creat_time
    role.update_time = update_time
    role.creat_id = creat_id
    role.update_id = update_id
    db.session.commit()
    roles = {
        'name': name,
        'creat_time': creat_time,
        'update_time': update_time,
        'creat_id': creat_id,
        'update_id': update_id
    }
    return jsonify(code=200, message='ok', data=roles)


# 注册修改角色路由
# 使用get_json()方法获取id
@role_bp.route('/role/modify3', methods=['PUT'])
@login_required
def role_modify3():
    data = request.get_json()
    if data is None:
        return jsonify(message=_('Invalid data.')), 400

    role = Role.query.get(data['id'])
    if role is None:
        return jsonify(message=_('Invalid role_id.')), 404

    role.name = data['name']
    role.creat_time = data['creat_time']
    role.update_time = data['update_time']
    role.creat_id = data['creat_id']
    role.update_id = data['update_id']
    db.session.commit()
    return jsonify(code=200, message='ok', data=data)


# 注册修改角色路由
# 使用form.get()方法获取id
@role_bp.route('/role/modify4', methods=['PUT'])
@login_required
def role_modify4():
    role_id = request.form.get('id')
    name = request.form.get('name')
    creat_time = request.form.get('creat_time')
    update_time = request.form.get('update_time')
    creat_id = request.form.get('creat_id')
    update_id = request.form.get('update_id')
    items = [name, creat_time, update_time, creat_id, update_id]
    for data in items:
        if data is None:
            return jsonify(message=_('Invalid data.')), 400

    role = Role.query.get(role_id)
    if role is None:
        return jsonify(message=_('Invalid role_id.')), 404

    role.name = name
    role.creat_time = creat_time
    role.update_time = update_time
    role.creat_id = creat_id
    role.update_id = update_id
    db.session.commit()
    roles = {
        'name': name,
        'creat_time': creat_time,
        'update_time': update_time,
        'creat_id': creat_id,
        'update_id': update_id
    }
    return jsonify(code=200, message='ok', data=roles)


# 注册角色查询路由
@role_bp.route('/role/query', methods=['POST'])
@login_required
def role_query():
    roles = Role.query.all()
    if roles is None:
        return jsonify(message=_('Invalid data.')), 404

    items = []
    for role in roles:
        item = {
            'name': role.name,
            'creat_time': role.creat_time,
            'update_time': role.update_time,
            'creat_id': role.creat_id,
            'update_id': role.update_id
        }
        items.append(item)

    return jsonify(code=200, message='ok', data=items)


# 注册删除单个角色路由
# 通过URL获取id
@role_bp.route('/role/<int:role_id>/delete1', methods=['DELETE'])
@login_required
def role_delete1(role_id):
    role = Role.query.get(role_id)
    if role is None:
        return jsonify(message=_('Invalid role_id.')), 404

    data = {
        'id': role.id,
        'name': role.name,
        'creat_time': role.creat_time,
        'update_time': role.update_time,
        'creat_id': role.creat_id,
        'update_id': role.update_id
    }
    db.session.delete(role)
    db.session.commit()
    return jsonify(code=200, message='ok', data=data)


# 注册删除单个路由
# 通过get_json()方法获取id
@role_bp.route('/role/delete2', methods=['DELETE'])
@login_required
def role_delete2():
    data = request.get_json()
    if data is None:
        return jsonify(message=_('Invalid data.')), 400

    role = Role.query.get(data['id'])
    if role is None:
        return jsonify(message=_('Invalid role_id.')), 404

    roles = {
        'id': role.id,
        'name': role.name,
        'creat_time': role.creat_time,
        'update_time': role.update_time,
        'creat_id': role.creat_id,
        'update_id': role.update_id
    }
    db.session.delete(role)
    db.session.commit()
    return jsonify(code=200, message='ok', data=roles)


# 注册删除单个角色路由
# 使用form.get()方法获取id
@role_bp.route('/role/delete3', methods=['DELETE'])
@login_required
def role_delete3():
    role_id = request.form.get('id')
    if role_id is None:
        return jsonify(message=_('Invalid role_id.')), 400

    role = Role.query.get(role_id)
    if role is None:
        return jsonify(message=_('Invalid role_id.')), 404

    roles = {
        'id': role.id,
        'name': role.name,
        'creat_time': role.creat_time,
        'update_time': role.update_time,
        'creat_id': role.creat_id,
        'update_id': role.update_id
    }
    db.session.delete(role)
    db.session.commit()
    return jsonify(code=200, message='ok', data=roles)


# 注册清空角色路由
# 使用for循环逐个清空
@role_bp.route('/role/clear1', methods=['DELETE'])
@login_required
def role_clear1():
    roles = Role.query.all()
    if roles is None:
        return jsonify(message=_('Invalid role_id.')), 404

    data = []
    for role in roles:
        item = {
            'id': role.id,
            'name': role.name,
            'creat_time': role.creat_time,
            'update_time': role.update_time,
            'creat_id': role.creat_id,
            'update_id': role.update_id
        }
        data.append(item)
        db.session.delete(role)

    db.session.commit()
    return jsonify(code=200,  message='ok', data=data)


# 注册清空角色路由
# 使用model(模型名).quer.delete()方法批量删除
@role_bp.route('/role/clear2', methods=['DELETE'])
@login_required
def role_clear2():
    Role.query.delete()
    db.session.commit()
    return jsonify(code=200, message='ok')