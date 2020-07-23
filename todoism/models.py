# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.

    ：建立数据库模型
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from todoism.extensions import db

# 创建User模型类，用来存储用户，用户和条目之间建立一对多关系
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)    # 主键字段
    username = db.Column(db.String(20), unique=True, index=True)    # 用户字段
    password_hash = db.Column(db.String(128))    # 密码散列值字段
    locale = db.Column(db.String(20))    # locale字段,用来存储区域代码,
    # 通过使用db.relationship()关系函数将items定义为关系属性,返回多个记录,关系函数中的第一个参数为另一侧的模型名称,
    # 通过设置back_populates参数的值为关系另一侧的关系属性名来连接对方,cascade参数是设置级联操作,其值设为'all'表示多个级联值的组合
    items = db.relationship('Item', back_populates='author', cascade='all')

    # 设置密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)    # 同一密码生成不同的密码散列值

    # 验证密码
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)    # 调用check_password_hash()函数检查密码散列值是否与设置的一致


# 创建Item模型类,用来存储待办条目,用户和条目之间建立一对多关系
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)     # 主键字段
    body = db.Column(db.Text)    # 主体字段
    done = db.Column(db.Boolean, default=False)    # 完成字段
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))    # author_id字段
    # 通过relationship()函数, 同时通过设置back_populates参数的值为关系另一侧的关系属性名来连接对方。
    author = db.relationship('User', back_populates='items')    # author字段
