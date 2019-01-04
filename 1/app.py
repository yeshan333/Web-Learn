'''
从flask包导入Flask类
'''
from flask import Flask
import click

# Flask类构造方法使用特殊变量__name__,
# python会根据所处的模块来赋予__name__变量相应的值
# 初始化一个Flask对象 
app = Flask(__name__)

# app.route()装饰器把根地址/和视窗函数index绑定起来
# 用户访问这个URL时就会触发index函数
@app.route('/')
def index():
	return '<h1>hello shansan</h1>'


@app.route('/1')
def hello():
	return '<h1>hello boy</h1>'

# 绑定多个URL
@app.route('/ye')
@app.route('/shan')
def shan():
	return '<h2>shansan</h2>'

# 动态URL
# 默认的name值为programmer
@app.route('/greet',defaults={'name':'programmer'})
@app.route('/greet/<name>')
def greet(name):
	return '<h1>hello ，%s ！</h1>'%name

'''
# 这段代码和上面那段效果相同
@app.route('/greet')
@app.route('/greet/<name>')
def greet(name = 'programmer'):
	return '<h1>hello ，%s ！</h1>'%name
'''



# 使用click模块的装饰器注册一个flask命令
@app.cli.command()
def hello():
	click.echo("hello flask !")





# 使用pipenv shell命令激活虚拟环境

# 使用flask shell可启动虚拟环境的python shell

# flask run命令用来启动内置的开发服务器（需要确保已激发了虚拟环境）

# 使用flask run --host=0.0.0.0使的服务器对外可见，处于同一个局域网内的用户都可以访问

# flask run --port=8000 改变默认端口



# .flaskenv用来设置环境变量(变量名为大写形式)

'''
- FLASK_RUN_HOST ：设置host
- FLASK_RUN_PORT ：改变默认端口
- FLASK_ENV ：设置运行环境，默认为生产(production)环境,
              开发环境: development
- FLASK_DEBUG ：调试器开关，1为开启，0为关闭 
'''
