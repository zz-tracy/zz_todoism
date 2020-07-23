# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.

    : 程序蓝本
"""
from flask import render_template, request, Blueprint, jsonify
from flask_babel import _
from flask_login import current_user, login_required

from todoism.extensions import db
from todoism.models import Item

# 实例化程序蓝本,并传入'todo'蓝本名,从__name__变量获取模块名todoism.blueprints.todo作为参数
todo_bp = Blueprint('todo', __name__)
# print('----', __name__)

# 使用todo_dp提供的route()装饰器以及登录依赖装饰器注册app视图函数,
@todo_bp.route('/app')
# login_required装饰器,确保当前用户在调用实际视图之前已登录并经过身份验证。（如果不是，则调用：attr:`LoginManager.unauthorized`回调。）
@login_required
def app():
    # 通过Item模型类的query属性进行查询,同时调用with_parent查询方法以及count()统计方法获取Item模型类中当前用户的条目总数量,
    # 存储到all_count变量中
    all_count = Item.query.with_parent(current_user).count()
    # 通过item模型类的query属性查询,同时调用with_parent()查询方法和filter_by()过滤方法,通过传入的done参数来过滤为完成条目,
    # 最后通过count()统计方法,返回为完成条目的数量,存储到active_count变量中
    active_count = Item.query.with_parent(current_user).filter_by(done=False).count()
    # 同上,最后返回已完成条目的数量,并存储到completed_count()变量中
    completed_count = Item.query.with_parent(current_user).filter_by(done=True).count()
    # 通过render_template()函数渲染模板,返回_app.html页面,同时传入items、all_count、active_count、completed_count参数
    # 其中'_app.html'是__app.html模板的路径
    # current_user.items是通过当前用户的User模型类的items关系属性,关联到当前用户的条目数据库表
    # all_count、active——count、completed_count分别为当前用户的条目总数,未完成条目数量,已完成条目数量
    return render_template('_app.html', items=current_user.items,
                           all_count=all_count, active_count=active_count, completed_count=completed_count)


# 使用todo_bp蓝本的route装饰器注册new_item视图函数
@todo_bp.route('/items/new', methods=['POST'])
# login_required装饰器,确保当前用户在调用实际视图之前已登录并经过身份验证。（如果不是，则调用：attr:`LoginManager.unauthorized`回调。）
@login_required
def new_item():
    # 通过调用resquest对象的json属性的get_json()函数,获取解析后的JSON数据,通过字典的方式获取键值
    data = request.get_json()
    # 判断data变量的值是否为空或者data变量所对应的字典中,'body'键对用的值是否为空
    if data is None or data['body'].strip() == '':
    # 如果为空,返回JSON格式的错误提示消息,以及错误状态码400
        return jsonify(message=_('Invalid item body.')), 400
    # 如果不为空,则实例化Item模型类,并传入data['body']键对应的值,以及通过_get_current_object()方法获取的当前对象的信息作为参数
    # 存储到item对象中
    item = Item(body=data['body'], author=current_user._get_current_object())
    db.session.add(item)    # 将item对象以参数的形式提交到数据库会话中
    db.session.commit()    # 提交数据库会话到数据库中
    # 通过render_template()函数渲染_item_html模板,并将此模板以参数的形式传递给jsonify()函数,同时该函数中的message参数,用来表示新条目的数量
    # 最后返回JSON格式的模板以及新条目的数量
    return jsonify(html=render_template('_item.html', item=item), message='+1')


# 注册编辑条目路由
@todo_bp.route('/item/<int:item_id>/edit', methods=['PUT'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)   # 传入item_id主键值作为参数,返回指定item_id主键值的记录,如果未找到,返回404错误响应
    if current_user != item.author:
        return jsonify(message=_('Permission denied.')), 403   # JSON格式的错误提示消息(权限被拒绝),403错误状态码

    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message=_('Invalid item body.')), 400
    item.body = data['body']
    db.session.commit()
    return jsonify(message=_('Item updated.'))


# 注册切换条目路由
@todo_bp.route('/item/<int:item_id>/toggle', methods=['PATCH'])
@login_required
def toggle_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message=_('Permission denied.')), 403

    item.done = not item.done
    db.session.commit()
    return jsonify(message=_('Item toggled.'))


# 注册删除条目路由
@todo_bp.route('/item/<int:item_id>/delete', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message=_('Permission denied.')), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify(message=_('Item deleted.'))


# 注册清除条目路由
@todo_bp.route('/item/clear', methods=['DELETE'])
@login_required
def clear_items():
    items = Item.query.with_parent(current_user).filter_by(done=True).all()
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return jsonify(message=_('All clear!'))
