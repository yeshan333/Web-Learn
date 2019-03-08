# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, redirect, Markup

app = Flask(__name__)

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