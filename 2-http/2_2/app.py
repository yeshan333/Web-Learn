'''
- 响应格式的设置
- MIME类型参考:http://www.w3school.com.cn/media/media_mimeref.asp
              - text/plain : 纯文本
              - text/html : html
              - application/json : json
              - text/xml : xml
'''

# -*- coding: utf-8 -*-

# 引入make_response方法
from flask import Flask, jsonify, request
from flask import make_response, redirect

app = Flask(__name__)


# 使用make_response方法生成响应对象
# 这个响应对象默认实例化内置的Response对象
# 参数为响应的主体
# 使用response对象的minetype属性设置MIME类型
@app.route('/foo')
def foo():
	response = make_response("Hello Flask")
	response.mimetype = 'text/plain'
	return response
	# return jsonify({"name": "shansan"})


# http://yourdomain/hello?name=shansan
# Cookie可以通过请求对象的cookies属性获取
@app.route('/')
@app.route('/hello')
def hello():
	name = request.args.get('name')
	if name == None:
		name = request.cookies.get('name','boy') # 默认值为boy
	return '<h1>Hello, %s</h1>' % name
    


# 使用set_cookie方法来设置cookie 
@app.route('/set/<name>')
def set_cookies(name):
	response = make_response(redirect('hello'))
	response.set_cookie('name', name)
	return response


