import os
import click
import sys

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)



# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

# 配置数据库URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 进行数据库操作前要先建表
# 注册创建数据库和表的flask命令
@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Initialized database.')

# 模型类(数据库表)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text) 

    """ def __repr__(self):
        return '<Note %r>' % self.body """

# new note
class NewNoteForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')

# edit note
class EditNoteForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Update')

# delete note
class DeleteNoteForm(FlaskForm):
    submit = SubmitField('Delete')


@app.route('/')
def index():
    form = DeleteNoteForm()
    notes = Note.query.all()
    # return render_template('index.html', notes=notes)
    return render_template('index.html', form=form, notes=notes)

@app.route('/new', methods=['POST', 'GET'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('Your note is saved.')
        return redirect(url_for('index'))
    return render_template('new_note.html', form=form)

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    form = EditNoteForm()
    # 获取要更新的笔记
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash('Your note is updated.')
        return redirect(url_for('index'))
    form.body.data = note.body
    return render_template('edit_note.html',form=form)

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        db.session.delete(note) # 删除记录
        db.session.commit()
        flash('Your note is deleted')
        return redirect(url_for('index'))
    else:
        abort(400)
    return redirect(url_for('index'))
    
