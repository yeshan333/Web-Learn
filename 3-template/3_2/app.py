# -*- coding: utf-8 -*-

from flask import Flask,url_for,redirect,render_template,Markup


user = {
	'username' : 'shansan',
	'bio': '我佛了',
}

movies = [
    { 'name': '我不是药神', 'year': '2018'},
    { 'name': '复仇者联盟3:无限战争', 'year': '2018'},
    { 'name': '原声之罪', 'year': '2018'},
]



app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', user=user, movies=movies)


@app.route('/watchlist')
def watchlist():
	return render_template('watchlist.html', user=user, movies=movies)

# 使用装饰器注册全局函数,给template使用
@app.template_global()
def bar():
	return 'I am bar.'


# 注册模板上下文处理函数(全局的),该函数需要返回一个包含变量键值对的字典
@app.context_processor
def inject_foo():
	foo = 'I an foo.'
	return dict(foo=foo)


@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')

# 自定义过滤器(filter)
# app.template_filter(name=musical)


@app.route('/base')
def base():
	return render_template('base.html')