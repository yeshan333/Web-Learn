'''
从flask包导入Flask类
'''
from flask import Flask
import click

# Flask类构造方法使用特殊变量__name__,
# python会根据所处的模块来赋予__name__变量相应的值 
app = Flask(__name__)

# app.route()装饰器把根地址/和视窗函数index绑定起来，
# 用户访问这个URL时就会触发index函数
@app.route('/1')
def index():
	return '<h1>hello shansan</h1>'

# 绑定多个URL
@app.route('/ye')
@app.route('/shan')
def shan():
	return '<h2>shansan</h2>'

# 动态URL
@app.route('/greet/<name>',defaults={'name':'programmer'})#默认的name值为programmer
def greet(name):
	return '<h1>hello ，%s ！</h1>'%name

# 使用flask shell
@app.cli.command()
def hello():
	click.echo("hello flask !")


# flask run命令用来启动内置的开发服务器（需要确保已激发了虚拟环境）

# .flaskenv用来设置环境变量


