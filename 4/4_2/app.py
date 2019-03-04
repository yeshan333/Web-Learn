# -*- coding: utf-8 -*-

import os
import uuid

from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session
from forms import LoginForm, UploadForm, MultiUploadForm
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')  # 设置CSRF令牌，默认为secret string
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True

# 指示保存上传后的文件的保存目录，路径通过app.root_path属性构造，文件名为uploads
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    # 验证表单是否是post提交，（PRG模式）
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)

@app.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('bootstrap.html', form=form)


# 使用内置的uuid库的方法uuid4()生成新的文件名，防止渗透
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success.')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)

# 获取上传后的文件，以便显示出来
@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

# 显示上传后的图片
@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')

# --------------------------------------------------------------------------
# 验证文件类型
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 多文件上传
@app.route('/multi-upload', methods=['POST', 'GET'])
def multi_upload():
    form = MultiUploadForm()
    if request.method == 'POST':
        filenames = []
        # 验证csrf令牌
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF ERROR !')
            return redirect(url_for('multi_upload'))
        # 检查文件是否存在
        if 'photo' not in request.files:
            flash('This file is required !')
            return redirect(url_for('multi_upload'))
        for f in request.files.getlist('photo'):
            #检查文件类型
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(
                    os.path.join(
                        app.config['UPLOAD_PATH'], filename)
                )
                # 将文件加到列表中
                filenames.append(filename)
            else:
                flash('invalid file type !')
                return redirect(url_for('multi_upload'))
        flash('Upload success.')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)




