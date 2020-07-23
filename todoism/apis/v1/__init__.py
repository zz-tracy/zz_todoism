# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import Blueprint
# 使用扩展flask_cors来为API添加跨域访问支持,
# 默认情况下,Flask-CORS会为蓝本下的所有路由添加跨域请求支持,并且允许来自任意源的跨域请求
from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)    # 实例化Blueprint()类,创建API蓝本

CORS(api_v1)    # 用于处理跨源资源共享（CORS），使得跨源AJAX成为可能。

# 导入resources模块,为了让蓝本和对应的视图关联起来
from todoism.apis.v1 import resources
