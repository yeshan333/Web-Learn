# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, redirect, Markup, flash

app = Flask(__name__)
# 由于通过flash函数发送的消息会存储在session对象中，所以需要设置密钥
app.secret_key = 'secret_string'

user = {
	'username' : 'shansan',
	'bio': '我佛了',
}

movies = [
    { 'name': '我不是药神', 'year': '2018'},
    { 'name': '复仇者联盟3:无限战争', 'year': '2018'},
    { 'name': '原声之罪', 'year': '2018'},
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/watchlist2')
def watchlist2():
    return render_template('watchlist2.html', user=user, movies=movies)

@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')

# 注册模板上下文处理函数(全局的),该函数需要返回一个包含变量键值对的字典
@app.context_processor
def inject_foo():
	foo = 'I an foo.'
	return dict(foo=foo)

@app.template_global()
def bar():
	return 'I am bar.'

# 消息闪现
@app.route('/flash')
def just_flash():
    flash("I m flash ,who is looking for me ?")
    return redirect(url_for('index'))

# *****************************************************
# 自定义错误页面

# 使用app.errorhandler()装饰器注册错误处理函数，该装饰器的参数为错误状态码
# 错误处理函数本身需要接收异常类作为参数，并在返回值中注明对应的http状态码
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500