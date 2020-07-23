# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.

    : 资源的序列化/响应的格式化/响应封装:将数据按照设计好的模式封装为json数据并返回
    : 序列化: 就是把数据库模型对象转换成JSON数据,
"""
from flask import url_for

from todoism.models import Item


# 定义生成表示用户资源的user_schema()函数,接收User类实例作为参数,该函数使用字典来定义资源的模式,返回按照预定模式创建的字典对象,用于生成JSON数据
def user_schema(user):
    return {
        'id': user.id,
        'self': url_for('.user', _external=True),    #  "self":表示资源自身的URL; _external=True表示允许外部访问
        'kind': 'User',                              # "kind":表示当前资源的类别
        'username': user.username,
        'all_items_url': url_for('.items', _external=True),
        'active_items_url': url_for('.active_items', _external=True),
        'completed_items_url': url_for('.completed_items', _external=True),
        'all_item_count': len(user.items),
        'active_item_count': Item.query.with_parent(user).filter_by(done=False).count(),
        'completed_item_count': Item.query.with_parent(user).filter_by(done=True).count(),
    }


# 定义生成表示单个条目资源的item_schema()函数,接收Item类实例作为参数,返回按照预定模式创建的字典对象,用于生成JSON数据
def item_schema(item):
    return {
        'id': item.id,
        'self': url_for('.item', item_id=item.id, _external=True), #"self":表示资源自身的URL; _external=True表示允许外部访问
        'kind': 'Item',                                            # "kind":表示当前资源的类别
        'body': item.body,
        'done': item.done,
        'author': {
            'id': 1,
            'url': url_for('.user', _external=True),
            'username': item.author.username,
            'kind': 'User',
        },
    }


# 定义生成表示集合条目资源的items_schema()函数,接收Item类实例,current, prev, next, pagination作为参数,
# 返回按照预定模式创建的字典对象,用于生成JSON数据
def items_schema(items, current, prev, next, pagination):
    return {
        'self': current,             #"self":表示资源自身的URL
        'kind': 'ItemCollection',    # "kind":表示当前资源的类别
        'items': [item_schema(item) for item in items],    # 迭代传入的ietms列表
        'prev': prev,
        'last': url_for('.items', page=pagination.pages, _external=True),
        'first': url_for('.items', page=1, _external=True),
        'next': next,
        'count': pagination.total
    }
