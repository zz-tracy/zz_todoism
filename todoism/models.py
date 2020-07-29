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
    # print('----', '测试断点1')
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
    # print('----', '测试断点2')
    id = db.Column(db.Integer, primary_key=True)     # 主键字段
    body = db.Column(db.Text)    # 主体字段
    done = db.Column(db.Boolean, default=False)    # 完成字段
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))    # author_id字段
    # 通过relationship()函数, 同时通过设置back_populates参数的值为关系另一侧的关系属性名来连接对方。
    author = db.relationship('User', back_populates='items')    # author字段


class SysUser(db.Model):
    # print('----', '测试断点3')
    """用户表"""
    # 主键
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, comment='主键')
    # 所属用户组
    user_group_id = db.Column(db.Integer, nullable=False, comment='所属用户组')
    # 用户名
    username = db.Column(db.String(64), nullable=False, comment='用户名')
    # 密码
    password = db.Column(db.String(64), nullable=False, comment='密码')
    # 盐值
    salt = db.Column(db.String(64), nullable=False, comment='盐值')
    # 姓名
    name = db.Column(db.String(64), nullable=False, comment='姓名')
    # 电话
    phone = db.Column(db.String(20), comment='电话')
    # 邮箱
    email = db.Column(db.String(64), comment='邮箱')
    # 创建时间
    creat_time = db.Column(db.DateTime, comment='创建时间', default=datetime.now)
    # 更新时间
    update_time = db.Column(db.DateTime, comment='更新时间', default=datetime.now)
    # 创建人
    creat_id = db.Column(db.Integer, comment='创建人')
    # 更新人
    update_id = db.Column(db.Integer, comment='更新人')
    # 登录时间
    login_time = db.Column(db.DateTime, comment='登录时间', default=datetime.now)
    # 上次登录时间
    last_login_time = db.Column(db.DateTime, comment='上次登录时间')
    # 登录次数
    login_count = db.Column(db.Integer, server_default=text('0'), comment='登录次数')


class Role(db.Model):
    # print('----', '测试断点4')
    """角色表"""
    # 主键
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='主键')
    # 角色名称
    name = db.Column(db.String(64), nullable=False, comment='角色名称')
    # 创建时间
    creat_time = db.Column(db.DateTime, comment='创建时间')
    # 更新时间
    update_time = db.Column(db.DateTime, comment='更新时间')
    # 创建人
    creat_id = db.Column(db.Integer, comment='创建人')
    # 更新人
    update_id = db.Column(db.Integer, comment='更新人')
    # 角色描述
    description = db.Column(db.String(200), comment='角色描述')


class Permission(db.Model):
    # print('----', '测试断点5')
    """权限表"""
    # 主键
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, comment='主键')
    # 模块
    model = db.Column(db.String(30), nullable=False, comment='模块')
    # 模块名称
    model_name = db.Column(db.String(50), nullable=False, comment='模块名称')
    # 操作
    action = db.Column(db.String(20), nullable=False, comment='操作')
    # 权限描述
    description = db.Column(db.String(128), comment='权限描述')
    # 创建时间
    creat_time = db.Column(db.DateTime, comment='创建时间')
    # 更新时间
    update_time = db.Column(db.DateTime, comment='更新时间')
    # 创建人
    creat_id = db.Column(db.Integer, comment='创建人')
    # 更新人
    update_id = db.Column(db.Integer, comment='更新人')

    @staticmethod
    def init_data():
        """ 初始权限 """
        """ 权限列表 """
        permissions = [
            {'id': 1, 'module': 'workspace', 'module_name': '空间', 'action': 'insert'},
            {'id': 2, 'module': 'workspace', 'module_name': '空间', 'action': 'update'},
            {'id': 3, 'module': 'workspace', 'module_name': '空间', 'action': 'select'},
            {'id': 4, 'module': 'workspace', 'module_name': '空间', 'action': 'delete'},
            {'id': 5, 'module': 'workspace', 'module_name': '空间', 'action': 'import'},
            {'id': 6, 'module': 'workspace', 'module_name': '空间', 'action': 'export'},

            {'id': 7, 'module': 'dashboard', 'module_name': '仪表盘', 'action': 'insert'},
            {'id': 8, 'module': 'dashboard', 'module_name': '仪表盘', 'action': 'update'},
            {'id': 9, 'module': 'dashboard', 'module_name': '仪表盘', 'action': 'select'},
            {'id': 10, 'module': 'dashboard', 'module_name': '仪表盘', 'action': 'delete'},
            {'id': 11, 'module': 'dashboard', 'module_name': '仪表盘', 'action': 'import'},
            {'id': 12, 'module': 'dashboard', 'module_name': '仪表盘', 'action': 'export'},

            {'id': 13, 'module': 'widget', 'module_name': '组件管理', 'action': 'insert'},
            {'id': 14, 'module': 'widget', 'module_name': '组件管理', 'action': 'update'},
            {'id': 15, 'module': 'widget', 'module_name': '组件管理', 'action': 'select'},
            {'id': 16, 'module': 'widget', 'module_name': '组件管理', 'action': 'delete'},
            {'id': 17, 'module': 'widget', 'module_name': '组件管理', 'action': 'import'},
            {'id': 18, 'module': 'widget', 'module_name': '组件管理', 'action': 'export'},

            {'id': 19, 'module': 'data_source', 'module_name': '数据源', 'action': 'insert'},
            {'id': 20, 'module': 'data_source', 'module_name': '数据源', 'action': 'update'},
            {'id': 21, 'module': 'data_source', 'module_name': '数据源', 'action': 'select'},
            {'id': 22, 'module': 'data_source', 'module_name': '数据源', 'action': 'delete'},
            {'id': 23, 'module': 'data_source', 'module_name': '数据源', 'action': 'import'},
            {'id': 24, 'module': 'data_source', 'module_name': '数据源', 'action': 'export'},

            {'id': 25, 'module': 'data_model', 'module_name': '数据模型', 'action': 'insert'},
            {'id': 26, 'module': 'data_model', 'module_name': '数据模型', 'action': 'update'},
            {'id': 27, 'module': 'data_model', 'module_name': '数据模型', 'action': 'select'},
            {'id': 28, 'module': 'data_model', 'module_name': '数据模型', 'action': 'delete'},
            {'id': 29, 'module': 'data_model', 'module_name': '数据模型', 'action': 'import'},
            {'id': 30, 'module': 'data_model', 'module_name': '数据模型', 'action': 'export'},

            {'id': 31, 'module': 'data_service', 'module_name': '数据服务', 'action': 'insert'},
            {'id': 32, 'module': 'data_service', 'module_name': '数据服务', 'action': 'update'},
            {'id': 33, 'module': 'data_service', 'module_name': '数据服务', 'action': 'select'},
            {'id': 34, 'module': 'data_service', 'module_name': '数据服务', 'action': 'delete'},
            {'id': 35, 'module': 'data_service', 'module_name': '数据服务', 'action': 'import'},
            {'id': 36, 'module': 'data_service', 'module_name': '数据服务', 'action': 'export'},

            {'id': 37, 'module': 'user_profile', 'module_name': '个人中心', 'action': 'insert'},
            {'id': 38, 'module': 'user_profile', 'module_name': '个人中心', 'action': 'update'},
            {'id': 39, 'module': 'user_profile', 'module_name': '个人中心', 'action': 'select'},
            {'id': 40, 'module': 'user_profile', 'module_name': '个人中心', 'action': 'delete'},
            {'id': 41, 'module': 'user_profile', 'module_name': '个人中心', 'action': 'import'},
            {'id': 42, 'module': 'user_profile', 'module_name': '个人中心', 'action': 'export'},

            {'id': 43, 'module': 'setting', 'module_name': '系统设置', 'action': 'insert'},
            {'id': 44, 'module': 'setting', 'module_name': '系统设置', 'action': 'update'},
            {'id': 45, 'module': 'setting', 'module_name': '系统设置', 'action': 'select'},
            {'id': 46, 'module': 'setting', 'module_name': '系统设置', 'action': 'delete'},
            {'id': 47, 'module': 'setting', 'module_name': '系统设置', 'action': 'import'},
            {'id': 48, 'module': 'setting', 'module_name': '系统设置', 'action': 'export'},
        ]
        for per in permissions:
            permission = Permission(id=per['id'], module=per['module'],
                                    module_name=per['module_name'], action=per['action'])
            db.session.add(permission)
        db.session.commit()


class UserGroup(db.Model):
    # print('----', '测试断点6')
    """用户组表"""
    # 主键
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # 用户组名称
    name = db.Column(db.String(64), nullable=False, comment='用户组名称')
    # 父用户组
    parent_id =db.Column(db.Integer, nullable=False, comment='父用户组')
    # 创建时间
    creat_time = db.Column(db.DateTime, comment='创建时间')
    # 更新时间
    update_time = db.Column(db.DateTime, comment='更新时间')
    # 创建人
    creat_id = db.Column(db.Integer, comment='创建人')
    # 更新人
    update_id = db.Column(db.Integer, comment='更新人')
    # 用户组描述
    description = db.Column(db.String(200), comment='用户组 描述')


class RolePermissionRelation(db.Model):
    # print('----', '测试断点7')
    """角色权限关联表"""
    # __tablename__ = 'sys_role_permission_relation'
    # __table_args__ =({'comment': '角色权限关联表'})
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, comment='主键')
    # 角色id
    role_id = db.Column(db.Integer, nullable=False, comment='角色id')
    # 权限id
    permission_id = db.Column(db.Integer, nullable=False, comment='权限id')


class UserRoleRelation(db.Model):
    # print('----', '测试断点8')
    """用户角色关联表"""
    # __tablename__ = "sys_user_role_relation"
    # __table_args__ = ({'comment': '用户角色关联表'})
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, comment="主键")
    # 用户id
    user_id =db.Column(db.Integer, nullable=False, comment='用户id')
    # 角色id
    role_id = db.Column(db.Integer, nullable=False, comment='角色id')


class UserGroupRoleRelation(db.Model):
    # print('----', '测试断点9')
    """用户组角色关联表"""
    # __tablename__ = "sys_user_group_role_relation"
    # __table_args__ = ({'comment': '用户组与角色关联表'})
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, comment='主键')
    # 角色id
    role_id = db.Column(db.Integer, nullable=False, comment='角色id')
    # 用户组id
    group_id = db.Column(db.Integer, nullable=False, comment='用户组id')


class UserGroupRelation(db.Model):
    # print('----', '测试断点10')
    """用户用户组关联表"""
    # __tablename__ = 'sys_user_group_relation'
    # __table_args__ = ({'comment': '用户用户组关联表'})
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, comment='主键')
    # 用户id
    user_id = db.Column(db.Integer, nullable=False, comment='用户id')
    # 用户组id
    group_id = db.Column(db.Integer, nullable=False, comment='用户组id')