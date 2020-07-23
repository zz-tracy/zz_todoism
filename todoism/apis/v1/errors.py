# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES    # werkzeug中的HTTP_STATUS_CODES字典,用来存储状态码和对应的原因短语的字典

from todoism.apis.v1 import api_v1


# 定义api_abort()错误响应处理函数,code参数为状态码,message参数用来指定错误提示消息,**kwargs参数为可变长度参数,用来接受其他的参数
def api_abort(code, message=None, **kwargs):
    if message is None:    # 验证message的值是否为None
        message = HTTP_STATUS_CODES.get(code, '')    # 从werkzeug中的HTTP_STATUS_CODES字典获取状态码的原因短语,使用状态码作为键

    response = jsonify(code=code, message=message, **kwargs)    # 调用jsonify()函数返回JSON数据字典,存储到response变量中
    response.status_code = code    # 使用code对response字典中的status_code键进行赋值
    return response  # You can also just return (response, code) tuple

#
def invalid_token():
    response = api_abort(401, error='invalid_token', error_description='Either the token was expired or invalid.')
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


def token_missing():
    response = api_abort(401)
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


class ValidationError(ValueError):    # 定义ValidationError异常类
    pass


# 为自定义异常类注册错误处理函数
# 使用Flask提供的errorhandler装饰器为ValidationError异常类注册一个错误处理函数,
# 当抛出和这个异常是时,处理函数就会被调用
@api_v1.errorhandler(ValidationError)
def validation_error(e):
    return api_abort(400, e.args[0])    # 使用api_abort()函数,返回400错误响应,同时接收异常类传入的参数作为错误消息
