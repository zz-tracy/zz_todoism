# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os

import click
from flask import Flask, render_template, jsonify, request, g
from flask_babel import _
# current_user 是werkzeug.local模块导入的LocalProxy类实例,LocalProxy用于代理Local对象和LocalStack对象，
# 而所谓代理就是作为中间的代理人来处理所有针对被代理对象的操作,主要目的是为了实现动态更新的效果
from flask_login import current_user

from todoism.apis.v1 import api_v1
from todoism.blueprints.auth import auth_bp
from todoism.blueprints.home import home_bp
from todoism.blueprints.todo import todo_bp
from todoism.blueprints.user import user_bp
from todoism.blueprints.user_bak import user_bak_bp
from todoism.blueprints.permission import permission_bp
from todoism.blueprints.role import role_bp
from todoism.extensions import db, login_manager, csrf, babel
from todoism.models import User, Item
from todoism.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
        # print('----', config_name)
        ''' 
        1. os模块是python标准库中的一个用于访问操作系统功能的模块， os模块提供了其他操作系统接口，可以实现跨平台访问
        2. os.getenv(‘PATH’, default) 获得指定的环境变量的内容
        3. 'FLASK_CONFIG'是配置变量  'development'是default默认值
        '''

    app = Flask('todoism')
    app.config.from_object(config[config_name])
    # app是程序实例 app.config中的config是Flask类中的属性,config[config_name]的config是配置文件config.py中导入的config字典
    # 将指定的配置通过from_object()方法导入到app.config字典配置对象中

    register_extensions(app)    # 注册扩展的初始化配置
    register_blueprints(app)    # 注册蓝本的初始化配置
    register_commands(app)    # 注册命令的初始化配置
    register_errors(app)    # 注册错误的初始化配置
    register_template_context(app)    # 注册模板上下文的初始化配置
    return app
    # 以上完成了实例化Flask以及Flask扩展的初始化配置


def register_extensions(app):
    # db: 是flask_sqlalchemy扩展中导入的SQLAlchemy的实例, 主要用于简化连接数据库服务器,管理数据库操作回话等工作
    db.init_app(app)    # 完成flask扩展的初始化安装
    # login_manager: 是flask_login扩展中导入的LoginManager类的实例,主要用于进行会话管理的相关操作，并完成用户合法性登陆和退出
    login_manager.init_app(app)    # 完成flask扩展的初始化安装
    # 此回调可用于初始化与此数据库设置一起使用。不要在上下文中使用数据库否则连接将泄漏。
    # csrf.init_app(app)
    # exempt()是csrf.py文件里CSRFProtect()类的一个方法,标记要从CSRF保护中排除的视图或蓝图。
    # 由于web API中的视图不需要使用CSRF防护,因为Web API并不使用cookie认证用户,所以使用csrf.exemp()方法取消对API蓝本的CSRF防护,
    # 该方法接受蓝本对象作为参数
    # csrf.exempt(api_v1)
    # babel是来实现程序的国际化和本地化;完成flask扩展的初始化安装
    babel.init_app(app)


def register_blueprints(app):
    @app.before_request
    def before_request():
        g.current_user = current_user

    app.register_blueprint(auth_bp)    # 使用register_blueprint()方法将auth_bp蓝本注册到程序实例上
    app.register_blueprint(todo_bp)    # 使用register_blueprint()方法将todo__bp蓝本注册到程序实例上
    app.register_blueprint(home_bp)    # 使用register_blueprint()方法将home_bp蓝本注册到程序实例上
    app.register_blueprint(user_bp)    # 使用register_blueprint()方法将user_bp蓝本注册到程序实例上
    app.register_blueprint(permission_bp)    # 使用register_blueprint()方法将permission_bp蓝本注册到程序实例上
    app.register_blueprint(role_bp)    # 使用register_blueprint()方法将role_bp蓝本注册到程序实例上
    app.register_blueprint(user_bak_bp)
    # 使用register_blueprint()方法将api_v1蓝本注册到程序实例上,其中第一个参数为蓝本名称,
    # 第二个参数为api_v1蓝本下的视图的URL前都会添加一个/api/v1前缀
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    # subdomain参数为api_v1蓝本指定子域,可以同事注册两次api_v1蓝本,分别支持通过子域或URL前缀的形式访问web API
    # app.register_blueprint(api_v1, url_prefix='/v1', subdomain='api')  # enable subdomain support(启用子域支持),


def register_template_context(app):
    @app.context_processor    # 上下文处理器: 让所有自定义变量在所有模板中全局可访问
    def make_template_context():
        if current_user.is_authenticated:    # 对current_user调用is_authenticated来判断当前用户是否登录
            # 通过对Item模型类的query属性对应的Query对象调用SQLAIchemy的with_parent()查询方法以及filter_by()过滤方法和count()查询方法
            # 对表中的记录进行筛选和调整,返回包含对应数据库记录数据的模型类实例,对返回的实例调用属性即可获取对应的字段数据.
            active_items = Item.query.with_parent(current_user).filter_by(done=False).count()
            # print(current_user)
        else:
            active_items = None
        return dict(active_items=active_items)


def register_errors(app):
    @app.errorhandler(400)    # 监听捕获异常 400:客户端请求的语法错误，服务器无法理解 Bad Request
    def bad_request(e):
        return render_template('errors.html', code=400, info=_('Bad Request')), 400    # 逗号前为flask返回的内容,400为返回的状态码

    @app.errorhandler(403)    # 监听捕获异常  403:服务器理解请求客户端的请求，但是拒绝执行此请求 Forbidden
    def forbidden(e):
        return render_template('errors.html', code=403, info=_('Forbidden')), 403

    @app.errorhandler(404)    # 监听捕获异常  404: 服务器无法根据客户端的请求找到资源（网页）。 Not Found
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html \
                or request.path.startswith('/api'):
            # 调用jsonify()函数,
            response = jsonify(code=404, message='The requested URL was not found on the server.')
            response.status_code = 404    # response通过调用status_code属性获取404状态码
            return response
        return render_template('errors.html', code=404, info=_('Page Not Found')), 404

    @app.errorhandler(405)    # 监听捕获异常  405: 客户端请求中的方法被禁止 Method Not Allowed
    def method_not_allowed(e):
        response = jsonify(code=405, message='The method is not allowed for the requested URL.')
        response.status_code = 405    # response通过调用status_code属性获取405状态码
        return response

    @app.errorhandler(500)    # 监听捕获异常 500: Internal Server Error 服务器内部错误，无法完成请求
    def internal_server_error(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html \
                or request.host.startswith('api'):
            response = jsonify(code=500, message='An internal server error occurred.')
            response.status_code = 500   # response通过调用status_code属性获取500状态码
            return response
        return render_template('errors.html', code=500, info=_('Server Error')), 500


def register_commands(app):
    @app.cli.command()  # 注册为命令
    # 设置选项,使用click提供的option装饰器为命令添加了一个--drop选项, 将is_flag参数设为True可以将这个选项声明为布尔值标志(booleanflag)
    @click.option('--drop', is_flag=True, help='Create after drop.')
    # --drop选项的值作为drop参数传入命令函数，如果提供了这个选项，那么drop的值将是True，否则为False。
    def initdb(drop):
        """Initialize the database."""  # 初始化数据库
        if drop:  # 判断是否输入了选项
            # 因为添加—drop选项会直接清空数据库内容,可以通过click.confirm()函数添加一个确认提示，这样只有输入y或yes才会继续执行操作。
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()  # 对数据库对象调用drop_all()方法清空数据库内容(包含数据和表结构)
            click.echo('Drop tables.')    # 输出提示消息
        db.create_all()  # 对数据库对象调用create_all()方法创建数据库表
        click.echo('Initialized database.')  # 输出提示信息复制代码

    # 使用app.cli.group()装饰器创建一个命令组,用来组织一系列翻译命令,其内容为空
    @app.cli.group()
    def translate():
        """Translation and localization commands."""    # 翻译和本地化命令。
        pass

    @translate.command()
    @click.argument('locale')
    # init()函数用来提取
    def init(locale):
        """Initialize a new language."""    # 初始化新语言。
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d todoism/translations -l ' + locale):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""    # 更新所有语言。
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d todoism/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""    # 编译所有语言
        if os.system('pybabel compile -d todoism/translations'):
            raise RuntimeError('compile command failed')
