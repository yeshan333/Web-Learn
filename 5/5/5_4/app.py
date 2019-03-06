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


""" # 进行数据库操作前要先建表
# 注册创建数据库和表的flask命令
@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Initialized database.') """

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
    
# --------------------------------------------------------------------------------
# 定义数据库模型类的关系


## 将db对象和模型类集成到Python Shell上下文中
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Note=Note, Author=Author, Article=Article, Book=Book, Writer=Writer,
                Country=Country, Capital=Capital, Teacher=Teacher, Student=Student)

## 一对多关系，单作者-多文章，外键不可少
## 外键(ForeignKey)总在多的那边,关系(relationship)总在单的那边

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    phone = db.Column(db.String(20))
    articles = db.relationship('Article') #articles为关系属性(一个集合，可以像列表一样操作)，在关系的出发侧定义

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(15), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))


## 双向关系，使用关系函数的back_populates参数

class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    books = db.relationship('Book', back_populates='writer')

    def __repr__(self):
        return '<Writer %r>' % self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    writer = db.relationship('Writer', back_populates='books')

    def __repr__(self):
        return '<Book %r>' % self.name

## 一对一关系，使用关系函数的uselist参数，将它设为False

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    capital = db.relationship('Capital', uselist=False)

class Capital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    country_id= db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country')

## 多对多关系，使用关联表（association table），关联表由db.Table定义
## 关系函数需要设置secondary参数，值为关系表名

association_table = db.Table('association',
                             db.Column('student_id', db.Integer, db.ForeignKey('teacher.id')),
                             db.Column('teacher_id', db.Integer, db.ForeignKey('student.id'))
                             )

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    grade = db.Column(db.String(20))
    teachers = db.relationship('Teacher', secondary=association_table,back_populates='students')


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    office = db.Column(db.String(20))
    students = db.relationship('Student', secondary=association_table, back_populates='teachers')



# ---------------------------------------------------------------------
# 更新数据库表

## 删表后重新生成表
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        click.confirm("This will delete the database, do you want to continue? ",abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo("Initialized database.")