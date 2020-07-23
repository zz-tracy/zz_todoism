# Todoism

*We are todoist, we use todoism.*

> Example application for *[Python Web Development with Flask](http://helloflask.com/en/book)* (《[Flask Web 开发实战](http://helloflask.com/book)》).

Demo: http://todoism.helloflask.com

![Screenshot](http://helloflask.com/screenshots/todoism.png)

## Installation  
--
clone:
```
$ git clone https://github.com/greyli/todoism.git
$ cd todoism
```
create & activate virtual env then install dependency:

with venv/virtualenv + pip:
```
$ python -m venv env  # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
$ pip install -r requirements.txt
```
or with Pipenv:
```
$ pipenv install --dev
$ pipenv shell
```
init database then run:
```
$ flask initdb
$ flask translate compile
$ flask run
* Running on http://127.0.0.1:5000/
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).



## 程序的项目结构使用功能式结构
## 程序包的目录结构如下

| 组件 | 说明 |  
| :----: | :----: |  
| todoism\ | 程序包 |  
| todoism\__init__.py | 构造文件,包含程序实例 |  
| todoism\extensions.py | 扩展文件,用来存储扩展实例化等操作 |  
| todoism\models.py | 数据库模型文件 |  
| todoism\settings.py | 配置文件 |  
| todoism\blueprints\__init__.py | 蓝本包的构造文件 为空(每一个包含__init__.py文件的文件夹都被视为包 |  
| todoism\blueprints\auth.py | 认证蓝本 |  
| todoism\buluprints\home.py | 主页蓝本 |  
| todoism\buluprints\home.py | 程序蓝本 |  
| todoism\templates\
| todoism\apis  | apis子包,用来存储API相关的脚本 |  
| todoism\apis\v1 | apis中的子包,表示API的某个版本(v1表示初始版本) |  
| 
