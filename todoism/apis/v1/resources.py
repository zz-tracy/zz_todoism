# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.

    : 创建资源类
"""
from flask import jsonify, request, current_app, url_for, g
from flask.views import MethodView    # 导入MethodView(方法视图)方法类,组织视图函数

from todoism.apis.v1 import api_v1
from todoism.apis.v1.auth import auth_required, generate_token
from todoism.apis.v1.errors import api_abort, ValidationError
from todoism.apis.v1.schemas import user_schema, item_schema, items_schema
from todoism.extensions import db
from todoism.models import User, Item

# 资源的反序列化:获取请求中包含的数据,然后验证数据的格式是否符合要求,最后存储与数据库中.
# 获取请求JSON中的body值
def get_item_body():
    data = request.get_json()    # 从request对象的get_json()方法中获取解析后的JSON数据
    # print(data)
    body = data.get('body')    # 使用键来获取对应的值
    # print(body)
    if body is None or str(body).strip() == '':    # 对数据进行验证,数据是否为空或者为None
        raise ValidationError('The item body was empty or invalid.')    # 跑出ValidationError异常
    return body


# 定义继承自MethodView的IndexAPI资源类,来组织get视图函数
class IndexAPI(MethodView):

# 定义get视图函数(一个资源首页),即根端点,该视图函数,返回API的版本信息,以及与所有主要资源对应的URL,作为API的主入口,
# 相当于API所提供资源的索引目录
    def get(self):
        return jsonify({
            "api_version": "1.0",
            "api_base_url": "http://example.com/api/v1",
            "current_user_url": "http://example.com/api/v1/user",
            "authentication_url": "http://example.com/api/v1/token",
            "item_url": "http://example.com/api/v1/items/{item_id }",
            "current_user_items_url": "http://example.com/api/v1/user/items{?page,per_page}",
            "current_user_active_items_url": "http://example.com/api/v1/user/items/active{?page,per_page}",
            "current_user_completed_items_url": "http://example.com/api/v1/user/items/completed{?page,per_page}",
        })


# 定义继承自MethodView的AuthTokenAPI资源类,,整个类表示一个资源端点(AuthTokenAPI)
class AuthTokenAPI(MethodView):

    def post(self):
        # print('----', 'nnnn')
        grant_type = request.form.get('grant_type')    # 从request请求表单中获取认证类型
        username = request.form.get('username')    # 从请求表单中获取用户名
        password = request.form.get('password')    # 从请求表单中获取密码


        # 验证认证类型
        if grant_type is None or grant_type.lower() != 'password':
            # print('----', 'cccc')
            # print(grant_type)
            # 调用api_abort()错误处理函数,传入code(状态码)和message(提示消息)参数,作为返回的错误状态码和错误消息提示
            return api_abort(code=400, message='The grant type must be password.')

        # 验证用户名及密码,
        user = User.query.filter_by(username=username).first()
        if user is None or not user.validate_password(password):
            return api_abort(code=400, message='Either the username or password was invalid.')

        token, expiration = generate_token(user)    # 调用generate_token()函数生成令牌,返回令牌及令牌有效时间别贝存储到token,expiration变量中

        response = jsonify({
            'access_token': token,    # 访问令牌
            'token_type': 'Bearer',    # 令牌类型:不记名令牌
            'expires_in': expiration    # 有效时间
        })
        # 由于返回的响应中包含令牌等敏感信息,所以将响应首部Cache-Control字段的值设为no-store
        # 将Pramaga字段的值设为no_cache
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Pragma'] = 'no-cache'
        return response


# 定义继承自MethodView的ItemAPI资源类,整个类表示一个资源端点(ItemPAI)
class ItemAPI(MethodView):
    # decorators = [auth_required]    # 使用flask在MethodView类中提供的decorators属性为整个资源类的所有视图方法附加装饰器,从而添加认证保护

# 获取指定资源的详细信息,采用JSON格式表现出来
    def get(self, item_id):
        """Get item."""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        # 使用模式函数获取资源字典,并传入对用的模型类实例作为参数,
        # 调用jsonify()方法将资源字典对象转换为标准的JSON数据,它会为响应报文设置正确的Content-Type字段(即'application/json')
        return jsonify(item_schema(item))

# 替换指定的集合成员,如果不存在则创建
    def put(self, item_id):
        """Edit item."""
        item = Item.query.get_or_404(item_id)
        # print('----', item)
        if g.current_user != item.author:
            print('----', '测试断点5')
            return api_abort(403)
        print('----', '测试断点6')
        item.body = get_item_body()
        db.session.commit()
        return '', 204

# 更新集合成员,仅提供更新的内容
    def patch(self, item_id):
        """Toggle item."""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        item.done = not item.done
        db.session.commit()
        return '', 204

# 删除指定的集合成员
    def delete(self, item_id):
        """Delete item."""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        db.session.delete(item)
        db.session.commit()
        return '', 204


# 定义继承自MethodView的UserAPI资源类,整个类表示一个资源端点(UserAPI)
class UserAPI(MethodView):
    # print('----', '测试断点1')
    # decorators = [auth_required]    # 使用flask在MethodView类中提供的decorators属性为整个资源类的所有视图方法附加装饰器,从而添加认证保护
    # print('----', auth_required)
# 传入的user_schema函数作为参数,返回按照预定模式创建的字典对象,该对象作为参数传递给jsonify()函数,最后返回当前用户的json数据
    def get(self):
        # print('----', '测试断点2')
        return jsonify(user_schema(g.current_user))


# 定义继承自MethodView的ItemsAPI资源类,整个类表示一个资源端点(ItemsAPI)
class ItemsAPI(MethodView):
    # decorators = [auth_required]    # 使用flask在MethodView类中提供的decorators属性为整个资源类的所有视图方法附加装饰器,从而添加认证保护

# 获取当前用户的所有条目,并对资源分页
    def get(self):
        """Get current user's all items."""
        # 从请求中获取请求的页码信息
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['TODOISM_ITEM_PER_PAGE']    # 配置per_page参数,来指定程序每页显示的条目数量
        # 通过对当前用户的所有条目调用paginate()方法,来设置用户条目的分页
        pagination = Item.query.with_parent(g.current_user).paginate(page, per_page)
        items = pagination.items    # 对pagination调用items实例,获取总页数,并存储到items变量中
        current = url_for('.items', page=page, _external=True)   # 定义当前页的URL
        prev = None    # 设置上一页的初始值为None
        # 对pagination调用has_prev()方法,来判断当前页面数是否大于1,返回true则进入if代码块
        if pagination.has_prev:
            prev = url_for('.items', page=page - 1, _external=True)    # 使用url_for()函数定义获取上一页的url
        next = None    # 设置下一页的初始值为None
        # 对pagination调用has_next()方法,来判断当前页是否是最后一页
        if pagination.has_next:
            next = url_for('.items', page=page + 1, _external=True)    # 使用url_for()函数定义获取下一页的url
        return jsonify(items_schema(items, current, prev, next, pagination))

    def post(self):
        """Create new item."""
        # 调用get_item_body()函数获取请求JSON中的body值,
        # 调用flask的全局变量g,获取当前用户
        # print('----', '断点3')
        item = Item(body=get_item_body(), author=g.current_user)
        # 将新创建的条目存储到数据库中
        db.session.add(item)
        db.session.commit()
        # 调用item_chema()模式函数,并传入item实例作为参数,返回按照预定模式创建的字典对象,
        # 调用jsonify()函数生成JSON数据,存储到response变量中
        response = jsonify(item_schema(item))
        response.status_code = 201    # 设置状态码201,表示已创建
        # 在响应头部的Location字段设置新创建条目的URL
        response.headers['Location'] = url_for('.item', item_id=item.id, _external=True)
        return response    # 返回新创建条目资源作为响应

# 定义继承自MethodView的ActiveItemsAPI资源类,整个类表示一个资源端点(ActiveItemsAPI)
class ActiveItemsAPI(MethodView):
    # decorators = [auth_required]    # 使用flask提供的MethonView类的decorators属性为整个资源类的所有视图方法添加装饰器,以达到认证保护的作用

    def get(self):
        """Get current user's active items."""
        page = request.args.get('page', 1, type=int)    # 从请求中
        pagination = Item.query.with_parent(g.current_user).filter_by(done=False).paginate(
            page, per_page=current_app.config['TODOISM_ITEM_PER_PAGE'])
        items = pagination.items
        current = url_for('.items', page=page, _external=True)
        prev = None
        if pagination.has_prev:
            prev = url_for('.active_items', page=page - 1, _external=True)
        next = None
        if pagination.has_next:
            next = url_for('.active_items', page=page + 1, _external=True)
        return jsonify(items_schema(items, current, prev, next, pagination))

# 定义继承自MethodView的CompletedItemsAPI资源类,整个类表示一个资源端点(CompletedItemsAPI)
class CompletedItemsAPI(MethodView):
    # decorators = [auth_required]    # 使用flask提供的MethonView类的decorators属性为整个资源类的所有视图方法添加装饰器,以达到认证保护的作用

    def get(self):
        """Get current user's completed items."""
        page = request.args.get('page', 1, type=int)
        pagination = Item.query.with_parent(g.current_user).filter_by(done=True).paginate(
            page, per_page=current_app.config['TODOISM_ITEM_PER_PAGE'])
        items = pagination.items
        current = url_for('.items', page=page, _external=True)
        prev = None
        if pagination.has_prev:
            prev = url_for('.completed_items', page=page - 1, _external=True)
        next = None
        if pagination.has_next:
            next = url_for('.completed_items', page=page + 1, _external=True)
        return jsonify(items_schema(items, current, prev, next, pagination))

    def delete(self):
        """Clear current user's completed items."""
        Item.query.with_parent(g.current_user).filter_by(done=True).delete()
        db.session.commit()  # TODO: is it better use for loop?
        return '', 204

# 使用add_url_rule()方法注册路由
# 由于整个资源类表示实现多个处理方法的视图,我们需要对资源类调用as_view()方法把其转换为视图函数,传入自定义的端点值(用来生成视图函数)
# 最后赋值给view_func参数
api_v1.add_url_rule('/', view_func=IndexAPI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
api_v1.add_url_rule('/user', view_func=UserAPI.as_view('user'), methods=['GET'])
api_v1.add_url_rule('/user/items', view_func=ItemsAPI.as_view('items'), methods=['GET', 'POST'])
api_v1.add_url_rule('/user/items/<int:item_id>', view_func=ItemAPI.as_view('item'),
                    methods=['GET', 'PUT', 'PATCH', 'DELETE'])
api_v1.add_url_rule('/user/items/active', view_func=ActiveItemsAPI.as_view('active_items'), methods=['GET'])
api_v1.add_url_rule('/user/items/completed', view_func=CompletedItemsAPI.as_view('completed_items'),
                    methods=['GET', 'DELETE'])
