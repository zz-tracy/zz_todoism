# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.

    :flask扩展文件
"""
from flask import request, current_app
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()   # 实例化SQLAlchemy()
# 实例化CSRFProtect(),在网站开发过程中要加入csrf保护
# CSRFProtect原理分析: 后端根据加密算法，生成csrf_token值，然后把csrf_token存储在session和g中，
# jinjia模版中根据{{ scrf_token }} 获取token值。
# 提交表单的时候，前端把token值和其他参数一起传回给后端，后端拿到值之后开始验证，如果和session中的值一致，就验证成功，否则验证失败。
csrf = CSRFProtect()    # 加入这行代码就可以起到csrf防护作用
babel = Babel()    # flask_babel是 flask的翻译扩展工具,其中Babel是python的一国际化工具包,与其对应的是translations文件,
                   # messages.pot 就是我们生成的翻译模板文件, translations文件夹是创建中文翻译的文件,
                   # 要确保 flask 能找到翻译内容，translations文件夹要和 templates 文件夹在同一个目录中。

# 通过从flask-login模块中导入LoginManager()类进行会话管理的相关操作，并完成用户合法性登陆和退出。
# 创建login_manager,并进行相关配置
login_manager = LoginManager()    # 实例化登录管理器
login_manager.login_view = 'auth.login'    # 认证登录
login_manager.login_message = _l('Please login to access this page.')    # 请登录以访问此页面

# 当没有sessionID时，通过装饰器指定的函数来读取用户到session中，达到在前端模板中调用当前登录用户current_user的目的
@login_manager.user_loader     # 通过调用用户登录管理器中的user_loader方法作为装饰器,该装饰器目的是将回调函数赋给self.user_callback
def load_user(user_id):
    from todoism.models import User
    return User.query.get(int(user_id))    # 返回通过对User模型类调用query查询属性以及get()方法获取的user_id的整数

# 调用babel实例的localeselector方法组成的装饰器注册一个获取当前用户本地的处理器
@babel.localeselector
def get_locale():
    # 判断当前用户是登录用户,且当前用户的区域代买不为空的情况下
    if current_user.is_authenticated and current_user.locale is not None:
        return current_user.locale    # 返回当前登录用户存储在数据库中的local字段
    # 如果是匿名用户,则在浏览器的cookie中获取匿名用户的区域代码存储到locale变量中
    locale = request.cookies.get('locale')
    # 判断locale不为空,则返回locale
    if locale is not None:
        return locale
    return request.accept_languages.best_match(current_app.config['TODOISM_LOCALES'])
