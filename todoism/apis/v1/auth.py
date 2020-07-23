# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.

    web API 认证处理文件
"""
from functools import wraps    # functools.wraps旨在消除装饰器对原函数造成的影响，即对原函数的相关属性进行拷贝，已达到装饰器不修改原函数的目的。

# g(程序上下文),替代Python的全局变量用法,确保仅在当前请求中可用。用于存储全局数据，每次请求都会重设
# current——app（程序上下文),指向处理请求的当前程序实例
# request(请求上下文),封装客户端发出的请求报文数据
from flask import g, current_app, request
#
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from todoism.apis.v1.errors import api_abort, invalid_token, token_missing
from todoism.models import User


# 生成令牌函数
def generate_token(user):
    expiration = 3600    # 令牌有效期
    # 实例化Serializer,并传入程序秘钥签名和expires_in作为参数
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': user.id}).decode('ascii')    #
    return token, expiration


def validate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return False
    user = User.query.get(data['id'])
    if user is None:
        return False
    g.current_user = user
    return True


def get_token():
    # Flask/Werkzeug do not recognize any authentication types
    # other than Basic or Digest, so here we parse the header by hand.
    if 'Authorization' in request.headers:
        try:
            token_type, token = request.headers['Authorization'].split(None, 1)
        except ValueError:
            # The Authorization header is either empty or has no token
            token_type = token = None
    else:
        token_type = token = None

    return token_type, token


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()

        # Flask normally handles OPTIONS requests on its own, but in the
        # case it is configured to forward those to the application, we
        # need to ignore authentication headers and let the request through
        # to avoid unwanted interactions with CORS.
        # 翻译: Flask通常独立处理OPTIONS请求，但是如果配置为将这些请求转发给应用程序，我们需要忽略身份验证头，
        # 让请求通过，以避免与CORS的不必要的交互。
        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'bearer':
                print(token_type)
                return api_abort(400, 'The token type must be bearer.')
            if token is None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()
        return f(*args, **kwargs)

    return decorated
