# coding: utf-8
""""
Приложение МИР Кино. Версия 1.0 с ограниченныйм функционалом.
Соловов М.А. Сочи, Сириус. Март 2020
"""
import os

from flask import Flask, render_template, redirect, jsonify
from flask import request, make_response, abort
from data import db_session

from data.users import User
from data.films import Films
from data.otzivi import Otziv
from data.rejiser import Rej
from data.janr import Janr
from data.novosti import Novosti
import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user
from flask_login import login_required, logout_user, current_user

from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'very_secret_password'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def choiseRejiser():
    ch_rej = []
    session = db_session.create_session()
    rej = session.query(Rej).all()
    for r_ in rej:
        ch_rej.append((r_.id, r_.name))
    if not ch_rej:
        ch_rej.append(('0','Нет данных'))
    return ch_rej

def choiseJanr():
    ch_janr = []
    session = db_session.create_session()
    jan = session.query(Janr).all()
    for r_ in jan:
        ch_janr.append((r_.id, r_.name))
    if not ch_janr:
        ch_janr.append(('0', 'Нет данных'))
    return ch_janr

class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    role = SelectField(u'Роль', choices=[('1', 'Пользователь'), ('2', 'Администратор')])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class NewfilmForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    year = IntegerField('Год выпуска', validators=[DataRequired()])
    #janr = SelectField(u'Жанр', choices=ch_janr)
    #rejiser = SelectField(u'Режисер', choices=ch_rejiser)
    about = TextAreaField("Краткое содержание", validators=[DataRequired()])
    pict = StringField('Обложка (файл)', validators=[DataRequired()])
    trail = StringField('Трейлер (ссылка)', validators=[DataRequired()])
    submit = SubmitField('Применить')

@app.route("/")
@app.route("/index")
def index():
    session = db_session.create_session()
    films = reversed(session.query(Films).filter(Films.is_serial != True).order_by(Films.id.desc()).limit(4).all())
    serials = reversed(session.query(Films).filter(Films.is_serial == True).order_by(Films.id.desc()).limit(4).all())
    novosti = reversed(session.query(Novosti).order_by(Novosti.id.desc()).limit(4).all())
    return render_template("index.html", title='Обзор Кино', films=films, serials=serials, novosti=novosti)


@app.route("/films")
def films():
    session = db_session.create_session()
    films = session.query(Films).filter(Films.is_serial != True)
    novosti = reversed(session.query(Novosti).order_by(Novosti.id.desc()).limit(4).all())
    return render_template("films.html", title='Фильмы', films=films, novosti=novosti)


@app.route("/serials")
def serials():
    session = db_session.create_session()
    films = session.query(Films).filter(Films.is_serial == True)
    novosti = reversed(session.query(Novosti).order_by(Novosti.id.desc()).limit(4).all())
    return render_template("serials.html", title='Сериалы', films=films, novosti=novosti)


@app.route("/show/<int:id>", methods=['GET', 'POST'])
def show_films(id):
    session = db_session.create_session()
    novosti = reversed(session.query(Novosti).order_by(Novosti.id.desc()).limit(4).all())
    film = session.query(Films).filter(Films.id == id).first()
    otz1 = []
    for item in session.query(Otziv).filter(Otziv.id_film == id).all():
        otz = {}
        otz["id"] = item.id
        user = session.query(User).filter(User.id == item.id_user).first()
        otz["user"] = user.name
        otz["otziv"] = item.otziv
        otz1.append(otz)
    otz = otz1
    rejiser = session.query(Rej).filter(Rej.id == film.rejiser).first()
    janr = session.query(Janr).filter(Janr.id == film.janr).first()
    return render_template("show.html", title=film.name, film=film, otziv=otz, rejiser=rejiser, janr=janr,
                           novosti=novosti)


@app.route("/reiting")
def reiting():
    session = db_session.create_session()
    films = session.query(Films).all()
    novosti = reversed(session.query(Novosti).order_by(Novosti.id.desc()).limit(4).all())
    return render_template("reiting.html", title='Рейтинг', films=films, novosti=novosti)


@app.route("/contact")
def contact():
    session = db_session.create_session()
    novosti = reversed(session.query(Novosti).order_by(Novosti.id.desc()).limit(4).all())
    return render_template("contact.html", title='Обратная связь', novosti=novosti)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/newfilm', methods=['GET', 'POST'])
@login_required
def newfilm():
    form = NewfilmForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        film = Films()
        film.year = form.year.data
        film.name = form.name.data
        film.pict = form.pict.data
        film.trail = form.trail.data
        film.about = form.about.data
        session.add(film)
        session.commit()
        return redirect('/')
    return render_template('newfilm.html', title='Добавление фильма', form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/kino.sqlite")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
