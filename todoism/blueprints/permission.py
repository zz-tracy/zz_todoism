# -*- coding: utf-8 -*-

"""
    :author: Dong Xiao (潇东)
    :url:
    :copyright:
    :license: MIT, see LICENSE for more details.

    权限接口
"""
from flask import request, Blueprint, jsonify
from flask_babel import _
from flask_login import login_required

from todoism.extensions import db
from todoism.models import Permission

permission_bp = Blueprint('permission', __name__)
# print('----', __name__)
# print('----', '测试断点2')


# 注册新增权限路由
@permission_bp.route('/permission/new1', methods=['POST'])
@login_required
def permission_new1():
    print('----', '测试断点1')
    data = request.get_json()  # 使用get_json()方法获取请求参数,返回一个包含请求参数的字典
    if data is None:
        return jsonify(message=_('Invalid permission data.')), 400

    permission = Permission(
        model=data['model'],
        model_name=data['model_name'],
        action=data['action'],
        description=data['description'],
        creat_time=data['creat_time'],
        update_time=data['update_time'],
        creat_id=data['creat_id'],
        update_id=data['update_id']
    )
    if permission is None:
        return jsonify(message=_('Invalid permission.')), 404

    db.session.add(permission)
    db.session.commit()
    return jsonify(code=200, message='ok', data=data)


# 注册新增用户权限
@permission_bp.route('/permission/new2', methods=['POST'])
@login_required
def permission_new2():
    # 使用request.form.get()方法通过传入Key键作为参数分别获取对应的请求参数值
    model = request.form.get('model')
    model_name = request.form.get('model_name')
    action = request.form.get('action')
    description = request.form.get('description')
    creat_time = request.form.get('creat_time')
    update_time = request.form.get('update_time')
    creat_id = request.form.get('creat_id')
    update_id = request.form.get('update_id')

    items = [model, model_name, action, description,  creat_time, update_time, creat_id, update_id]
    for data in items:
        if data is None:
            return jsonify(message=_('Invalid data')), 400

    permission = Permission(
        model=model,
        model_name=model_name,
        action=action,
        description=description,
        creat_time=creat_time,
        update_time=update_time,
        creat_id=creat_id,
        update_id=update_id
    )
    db.session.add(permission)
    db.session.commit()
    permissions = {
        'model': model,
        'model_name': model_name,
        'action': action,
        'description': description,
        'creat_time': creat_time,
        'update_time': update_time,
        'creat_id': creat_id,
        'update_id': update_id
    }
    return jsonify(code=200, message='ok', data=permissions)


# 注册修改权限路由
# 通过URL获取ID
@permission_bp.route('/permission/<int:permission_id>/modify1', methods=['PUT'])
@login_required
def permission_modify1(permission_id):
    permission = Permission.query.get(permission_id)
    if permission is None:
        return jsonify(message=_('Invalid permission_id.')), 404

    # 使用get_json()方法获取请求参数
    data = request.get_json()
    if data is None:
        return jsonify(message=_('Invalid data.')), 400

    permission.model = data['model']
    permission.model_name = data['model_name']
    permission.action = data['action']
    permission.description = data['description']
    permission.creat_time = data['creat_time']
    permission.update_time = data['update_time']
    permission.creat_id = data['creat_id']
    permission.update_id = data['update_id']
    db.session.commit()
    return jsonify(code=200, message='ok', data=data)


# 注册权限修改路由
@permission_bp.route('/permission/<int:permission_id>/modify2', methods=['PUT'])
@login_required
def permission_modify2(permission_id):
    permission = Permission.query.get(permission_id)
    if permission is None:
        return jsonify(message=_('Invalid permission.')), 404

    # 使用request.form.get()方法获取参数
    model = request.form.get('model')
    model_name = request.form.get('model_name')
    action = request.form.get('action')
    description = request.form.get('description')
    creat_time = request.form.get('creat_time')
    update_time = request.form.get('update_time')
    creat_id = request.form.get('creat_id')
    update_id = request.form.get('update_id')
    items = [model, model_name, action, description,  creat_time, update_time, creat_id, update_id]
    for data in items:
        if data is None:
            return jsonify(message=_('Invalid data.')), 400

    permissions = {
        'model': model,
        'model_name': model_name,
        'action': action,
        'description': description,
        'creat_time': creat_time,
        'update_time': update_time,
        'creat_id': creat_id,
        'update_id': update_id
    }

    permission.model = model
    permission.model_name = model_name
    permission.action = action
    permission.description = description
    permission.creat_time = creat_time
    permission.update_time = update_time
    permission.creat_id = creat_id
    permission.update_id = update_id
    db.session.commit()
    return jsonify(code=200, message='ok', data=permissions)


# 注册权限修改路由
# 通过get_json()方法获取id
@permission_bp.route('/permission/modify3', methods=['PUT'])
@login_required
def permission_modify3():
    data = request.get_json()
    if data is None:
        return jsonify(message=_('Invalid data.')), 400

    permission = Permission.query.get(data['id'])
    print('----', permission)
    if permission is None:
        return jsonify(message=_('Invalid permission_id.')), 404

    permission.model = data['model']
    permission.model_name = data['model_name']
    permission.action = data['action']
    permission.description = data['description']
    permission.creat_time = data['creat_time']
    permission.update_time = data['update_time']
    permission.creat_id = data['creat_id']
    permission.update_id = data['update_id']
    db.session.commit()
    return jsonify(code=200, message='ok', data=data)


# 注册权限修改路由
# 使用request.form.get()方法获取id
@permission_bp.route('/permission/modify4', methods=['PUT'])
@login_required
def permission_modify4():
    permission_id = request.form.get('id')
    model = request.form.get('model')
    model_name = request.form.get('model_name')
    action = request.form.get('action')
    description = request.form.get('description')
    creat_time = request.form.get('creat_time')
    update_time = request.form.get('update_time')
    creat_id = request.form.get('creat_id')
    update_id = request.form.get('update_id')
    items = [permission_id, model, model_name, action, description, creat_time, update_time, creat_id, update_id]
    for data in items:
        if data is None:
            return jsonify(message=_('Invalid data.')), 400

    permission = Permission.query.get(permission_id)
    if permission is None:
        return jsonify(message=_('Invalid permission_id.')), 404

    permissions = {
        'id': permission_id,
        'model': model,
        'model_name': model_name,
        'action': action,
        'description': description,
        'creat_time': creat_time,
        'update_time': update_time,
        'creat_id': creat_id,
        'update_id': update_id
    }
    permission.model = model
    permission.model_name = model_name
    permission.action = action
    permission.description = description
    permission.creat_time = creat_time
    permission.update_time = update_time
    permission.creat_id = creat_id
    permission.update_id = update_id
    db.session.commit()
    return jsonify(code=200, message='ok', data=permissions)


# 注册权限查询路由
@permission_bp.route('/permission/query', methods=['POST'])
@login_required
def permission_query():
    permissions = Permission.query.all()
    if permissions is None:
        return jsonify(message=_('Invalid permission.')), 404

    data = []
    for permission in permissions:
        item = {
            'model': permission.model,
            'model_name': permission.model_name,
            'action': permission.action,
            'description': permission.description,
            'creat_time': permission.creat_time,
            'update_time': permission.update_time,
            'creat_id': permission.creat_id,
            'update_id': permission.update_id
        }
        data.append(item)
    return jsonify(code=200, message='ok', data=data)


# 注册删除单个权限路由
# 通过URL获取id
@permission_bp.route('/permission/<int:permission_id>/delete1', methods=['DELETE'])
@login_required
def permission_delete1(permission_id):
    permission = Permission.query.get(permission_id)
    if permission is None:
        return jsonify(message=_('Invalid permission_id.')), 404

    permissions = {
        'id': permission.id,
        'model': permission.model,
        'model_name': permission.model_name,
        'action': permission.action,
        'description': permission.description,
        'creat_time': permission.creat_time,
        'update_time': permission.update_time,
        'creat_id': permission.creat_id,
        'update_id': permission.update_id
    }
    db.session.delete(permission)
    db.session.commit()
    return jsonify(code=200, message='ok', data=permissions)


# 注册删除单个权限路由
# 使用get_json()方法获取id
@permission_bp.route('/permission/delete2', methods=['DELETE'])
@login_required
def permission_delete2():
    permission_id = request.get_json()
    if permission_id is None:
        return jsonify(message=_('Invalid permission_id.')), 400

    permission = Permission.query.get(permission_id['id'])
    if permission is None:
        return jsonify(message=_('Invalid permission_id.')), 404

    permissions = {
        'id': permission.id,
        'model': permission.model,
        'model_name': permission.model_name,
        'action': permission.action,
        'description': permission.description,
        'creat_time': permission.creat_time,
        'update_time': permission.update_time,
        'creat_id': permission.creat_id,
        'update_id': permission.update_id
    }
    db.session.delete(permission)
    db.session.commit()
    return jsonify(code=200, message='ok', data=permissions)


# 注册删除单个权限路由
# 使用form.get()方法获取id
@permission_bp.route('/permission/delete3', methods=['DELETE'])
@login_required
def permission_delete3():
    permission_id = request.form.get('id')
    if permission_id is None:
        return jsonify(message=_('Invalid permission_id.')), 400

    permission = Permission.query.get(permission_id)
    if permission is None:
        return jsonify(message=_('Invalid permission_id.')), 404

    permissions = {
        'id': permission.id,
        'model': permission.model,
        'model_name': permission.model_name,
        'action': permission.action,
        'description': permission.description,
        'creat_time': permission.creat_time,
        'update_time': permission.update_time,
        'creat_id': permission.creat_id,
        'update_id': permission.update_id
    }
    db.session.delete(permission)
    db.session.commit()
    return jsonify(code=200, messgae='ok', data=permissions)


# 注册清空(逐个删除)权限路由
# 使用for循环,在循环体内逐个删除权限记录
@permission_bp.route('/permission/clear1', methods=['DELETE'])
@login_required
def permission_clear1():
    permissions = Permission.query.all()
    if permissions is None:
        return jsonify(message=_('Invalid permission_id.')), 400

    items = []
    for permission in permissions:
        data = {
            'id': permission.id,
            'model': permission.model,
            'model_name': permission.model_name,
            'action': permission.action,
            'description': permission.description,
            'creat_time': permission.creat_time,
            'update_time': permission.update_time,
            'creat_id': permission.creat_id,
            'update_id': permission.update_id
        }
        items.append(data)
        db.session.delete(permission)

    db.session.commit()
    return jsonify(code=200, message='ok', data=items)


# 注册清空(批量)权限路由
# 使用model(模型名).query.delete()
@permission_bp.route('/permission/clear2', methods=['DELETE'])
@login_required
def permission_clear2():
    Permission.query.delete()
    db.session.commit()
    return jsonify(code=200, message='ok')

