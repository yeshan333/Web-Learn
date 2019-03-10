# 模拟用户登录
# 模拟后台管理
# -*- coding: utf-8 -*-

from flask import Flask,session,request,url_for,redirect,abort
import os


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')

# 操控session和操控字典差不多，pop方法和clear方法可以清除session，用get方法获取session
# app.config['SECRET_KEY'] = os.urandom(24) # 随机生成24位的SECRET_KEY，每次重启服务器的时候都不一样，这样就会影响session的解密

# sessiond的过期时间说明
## 默认过期时间为浏览器关闭后，通过session.permanent = True设置过期时间为一个月
### 通过app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7) 可自由设置过期时间


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