# -*_-coding: utf-8 -*-

from flask import Flask,render_template,url_for

# 字典
user = {
	'username': 'Sam Ye',
	'info': '乐呵！！！！！！',
}


# 命名要规范
ga = [
	{'name': 'zzz', 'year': '未知'},
	{'name': 'wwww', 'year': '未知'},
	{'name': 'sss', 'year': '未知'},
	{'name': 'qqq', 'year': '等等'},
]


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games')
def games():
	return render_template('games.html', user=user, ga=ga)