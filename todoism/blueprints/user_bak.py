from flask import render_template, request, Blueprint, jsonify
from flask_babel import _
from flask_login import current_user, login_required
from sqlalchemy import and_, or_

from todoism.extensions import db
from todoism.models import SysUser

user_bak_bp = Blueprint('user_bak', __name__)
# print('----', __name__)


# 使用filter()方法注册查询路由
@user_bak_bp.route('/user2', methods=['POST'])
@login_required
def query_user2():
    data = request.get_json()
    print('----', data)
    print('----', data['name'])
    if data is None \
            or data['name'].strip() == '':
        return jsonify(message=_('Invalid data.')), 400

    # 使用filter()过滤方法及"=="查询操作符进行查询
    users = SysUser.query.filter(SysUser.name == data['name']).first()
    # print('----', users)
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 使用filter()过滤方法及'!='查询操作符进行查询
    users = SysUser.query.filter(SysUser.name != data['name']).first()
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 使用filter()过滤方法及'like(区分大小写, 模糊查询)'查询操作符进行查询
    hello = request.get_json()['hello']
    users = SysUser.query.filter(SysUser.username.like('%' + hello + '%')).all()
    print('----', users)
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 使用filter()过滤方法及'ilike(不区分大小写)'
    hello = request.get_json()['hello']
    users = SysUser.query.filter(SysUser.username.ilike('%' + hello + '%')).all()
    print('----', users)
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 使用filter()过滤方法及'in'查询操作符进行查询
    users = SysUser.query.filter(SysUser.name.in_(data['names'])).all()
    print('----', users)
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 使用filter()过滤方法及'not in'查询操作符进行查询
    users = SysUser.query.filter(SysUser.name.notin_(data['names'])).all()
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 使用and_()
    users = SysUser.query.filter(and_(SysUser.name == data['name'], SysUser.username == data['username'])).all()
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 在filter()中加入多个表达式,使用逗号分隔,表示表示同时满足两个表达式的数据
    users = SysUser.query.filter(SysUser.name == data['name'], SysUser.username == data['username']).all()
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 在filter()方法中叠加调用多个filter()方法
    users = SysUser.query.filter(SysUser.name == data['name']).filter(SysUser.username == data['username']).all()
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 在filter()方法中使用or_()
    users = SysUser.query.filter(or_(SysUser.name == data['name'], SysUser.username == data['username'])).all()
    # print('----', users)
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 使用order_by()方法进行正排序
    users = SysUser.query.order_by('age').all()
    print('----', users)
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 使用order_by()方法进行倒排序
    users = SysUser.query.order_by(and_(SysUser.age.desc())).all()
    # print('----', users)
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 通过db.session使用order_by()方法进行单字段正排序
    users = db.session.query(SysUser.age, SysUser.name, SysUser.username).order_by('age').all()
    # print('----', users)
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    # 通过db.session使用order_by()方法进行单字段倒排序
    users = db.session.query(SysUser.age, SysUser.name, SysUser.username).order_by(SysUser.age.desc()).all()
    # print('----', users)
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    items = []
    for user in users:
        item2 = {
            'gender': user.gender,
            'age': user.age,
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
        items.append(item2)
    item2 = {
            'gender': users.gender,
            'user_group_id': users.id,
            'username': users.username,
            'password': users.password,
            'salt': users.salt,
            'name': users.name,
            'phone': users.phone,
            'email': users.email,
            'creat_id': users.creat_id,
            'update_id': users.update_id,
            'last_login_time': users.last_login_time,
            'login_count': users.login_count
        }
    return jsonify(code=200, message='ok', data=users)


# 查询----使用paginate()方法实现分页功能
@user_bak_bp.route('/user3', methods=['POST'])
@login_required
def query_user3():
    data = request.get_json()
    page = data['page']
    print('----', page)
    page_size = data['page_size']
    print('----', page_size)
    # 一页多少条:page_size, 当前第几页: page
    users = db.session.query(SysUser.age, SysUser.name, SysUser.username)\
        .order_by(SysUser.age.desc()).paginate(page, page_size)
    print('----', db.session.query(SysUser.age, SysUser.name, SysUser.username).order_by(SysUser.age.desc()))
    print('---', users.items)
    items = users.items
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    return jsonify(code=200, message='ok', data=items)


# 查询----使用limit()和offset()方法实现分页功能
@user_bak_bp.route('/user4', methods=['POST'])
@login_required
def query_user4():
    data = request.get_json()
    page = data['page']
    page_size = data['page_size']
    users = db.session.query(SysUser.age, SysUser.username, SysUser.name).limit(page_size).offset(page).all()
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    return jsonify(code=200, message='ok', data=users)


# 查询--多字段排序
@user_bak_bp.route('/user5', methods=['POST'])
@login_required
def query_user5():
    # data = request.get_json()
    # if data is None:
    #     return jsonify(message=_('Invalid data.')), 400

    users = db.session.query(SysUser.age, SysUser.username, SysUser.gender).order_by('age', 'gender').all()
    print('----', users)
    if users is None:
        return jsonify(message=_('Invalid users.')), 404

    items = []
    for item in users:
        user = {
            'gender': item.gender,
            'age': item.age,
            # 'user_group_id': item.id,
            'username': item.username,
            # 'password': item.password,
            # 'salt': item.salt,
            # 'name': item.name,
            # 'phone': item.phone,
            # 'email': item.email,
            # 'creat_id': item.creat_id,
            # 'update_id': item.update_id,
            # 'last_login_time': item.last_login_time,
            # 'login_count': item.login_count
        }
        items.append(user)

    print('----', items)
    return jsonify(code=200, message='ok', data=items)


# 查询----分组
@user_bak_bp.route('/user6', methods=['POST'])
@login_required
def query_user6():
    # data = request.get_json()
    # if data is None:
    #     return jsonify(message=_('Invalid data.')), 400

    users = SysUser.query.group_by('gender').all()
    print('----', users)
    items = []
    for item in users:
        user = {
            'gender': item.gender,
            'age': item.age,
            # 'user_group_id': item.id,
            'username': item.username,
            # 'password': item.password,
            # 'salt': item.salt,
            # 'name': item.name,
            # 'phone': item.phone,
            # 'email': item.email,
            # 'creat_id': item.creat_id,
            # 'update_id': item.update_id,
            # 'last_login_time': item.last_login_time,
            # 'login_count': item.login_count
        }
        items.append(user)

    return jsonify(code=200, message='ok', data=items)