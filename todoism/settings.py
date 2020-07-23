# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os

# os.path.dirname(__file__)返回当前运行脚本的绝对路径,
# os.path.dirname(os.path.dirname(__file__)),获取当前运行脚本的绝对路径(去掉最后一个路径)
# os.path.abspath()返回.py文件的绝对路径
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# print('----', __file__)
# print('----', os.path.dirname(__file__))
# print('----', os.path.dirname(os.path.dirname(__file__)))
# print('----', basedir)


# 创建基础配置BaseConfig类
class BaseConfig:
    TODOISM_LOCALES = ['en_US', 'zh_Hans_CN']    # 配置程序本地语言
    TODOISM_ITEM_PER_PAGE = 20     # 配置程序每页显示条目的数量

    BABEL_DEFAULT_LOCALE = TODOISM_LOCALES[0]    # 配置程序本地默认的语言环境为'en_US'

    # SERVER_NAME = 'todoism.dev:5000'  # enable subdomain support(启用子域支持)
    SECRET_KEY = os.getenv('SECRET_KEY', 'a secret string')    # 配置密钥,默认是'a secret string'

    # 通过配置变量SQLALCHEMY_DATABASE_URI设置数据库URI,默认为SQLite内存型数据库(sqlite:///)
    # 使用app.root_path来定位数据库文件的路径,并将数据库文件命名为data.db
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.db'))

    # 在生产环境下更换到其他类型的DBMS(数据库管理系统)时,数据库URL会包含敏感信息,所以这里优先从环境变量DATABASE_URL获取
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:123456@127.0.0.1:5432/postgres')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:zyd@6434@127.0.0.1:3306/todoism')
    # Flask-SQLAlchemy有自己的事件通知系统，该系统在SQLAlchemy之上分层。为此，它跟踪对SQLAlchemy会话的修改。这会占用额外的资源，
    # 因此该选项SQLALCHEMY_TRACK_MODIFICATIONS允许你禁用修改跟踪系统。
    # 当前，该选项默认为True，但将来该默认值将更改为False，从而禁用事件系统。
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # 关闭Flask-SQLAlchemy事件系统（并禁用警告）


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


# 创建TestingConfig测试类
class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    WTF_CSRF_ENABLED = False

# 配置程序config字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
