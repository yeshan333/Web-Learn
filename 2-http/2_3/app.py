# 模拟用户登录
# 模拟后台管理
# -*- coding: utf-8 -*-

from flask import Flask,session,request,url_for,redirect,abort
import os


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')

# 登陆
@app.route('/login')
def login():
	session['logged_in'] = True
	return redirect(url_for('hello'))

# 登出
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


@app.route('/')
@app.route('/hello')
def hello():
	name = request.args.get('name')
	if name == None:
		name = request.args.get('name','gay')
		response = '<h1>hello %s</h1>' % name
	# 根据用户认证状态返回不同的内容
	# 判断session中是否存在logged_in键
	if 'logged_in' in session:
		response += '登陆成功'
	else:
		response += '登陆失败'
	return response

@app.route('/admin')
def admin():
	if 'logged_in' not in session:
		abort(403)
	return 'Welcome to admin page'