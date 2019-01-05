# -*- coding: utf-8 -*-

# 引入flask库中的request类,重定向函数redirect
# url_for函数用于获取URL，第一个参数为端点，一般为视函数名
from flask import Flask,request,redirect,url_for

app = Flask(__name__)

# 访问根目录时，重定向到/hello目录
@app.route('/')
def index():
	return redirect(url_for('hello'))


# 重定向的另一种食用方法
# Location字段设置了重定向的目标URL
# 3XX重定向响应
@app.route('/test')
def fole():
	return '', 302, {'Location': 'https://shansan.top'}



@app.route('/hello')
def hello():
	# 使用request对象的get()方法获取查询参数name的值
	# request对象的args属性用于存储查询字符串
	# get()方法的第二个参数为默认值
	# 不设置默认参数，如果没有获取到name的值，会返回HTTP 400错误
	name = request.args.get('name', 'Flask')
	return '<p align="middle"><strong>hello %s</strong><p>' % name


# 这里使用了装饰器的methods参数，传入了一个包含监听HTTP方法的可迭代对象
# 当请求方法不符合要求时，会返回405错误
@app.route('/http',methods=['GET', 'POST'])
def wocao():
	return '<ul>wocao<ul><br><ul>emmmm<ul>'



# 使用了URL规则
# 为year变量提供了int转换器
@app.route('/goback/<int:year>')
def go_back(year):
	return '<h1><strong>%d年距今%d年</strong></h1>'%(year, 2019-year)




# 使用flask routes命令可以查看程序中定义的所有路由

