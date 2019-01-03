'''
从flask包导入Flask类
'''
from flask import Flask

# 
app = Flask(__name__)

@app.route('/')

def index():
	return '<h1>hello shansan</h1>'