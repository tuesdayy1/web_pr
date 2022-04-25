from flask import Flask, request, url_for, render_template, \
    redirect
from random import randrange
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
import os
from flask_login import LoginManager, login_user, login_required, logout_user
import flask_login


app = Flask(__name__, template_folder='templates')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['POST', 'GET'])
def main():
    nums = []
    if request.method == 'GET':
        from_ = 1
        before = 100
        if 'flask_login.mixins.AnonymousUserMixin' in str(flask_login.current_user):
            return f'''<!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                        </head>
                        <body>
                            <form class="form-group" method="post">
                                <div class="alert alert-primary" role="alert">
                                    <a href="http://127.0.0.1:8080/login">Войти</a>
                                </div>
                                <center>
                                    <h1>{randrange(from_, before)}</h1>
                                    <input type="text"
                                        class="form-control"
                                        autocomplete="off"
                                        placeholder="first number"
                                        name="from"
                                        value="{from_}">
                                    <input type="text"
                                        class="form-control"
                                        autocomplete="off"
                                        placeholder="second number"
                                        name="before"
                                        value="{before}">
                                    <button type="submit" class="btn btn-primary">Generate</button>
                                </center>
                            </form>
                        </body>
                    </html>'''
        else:
            return f'''<!DOCTYPE html>
                                <html lang="en">
                                    <head>
                                        <meta charset="utf-8">
                                        <link rel="stylesheet"
                                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                                    </head>
                                    <body>
                                        <form class="form-group" method="post">
                                            <div class="alert alert-primary" role="alert">
                                                <h4>{flask_login.current_user.name}</h4>
                                                <a href="http://127.0.0.1:8080/logout">Выйти</a>
                                            </div>
                                            <center>
                                                <h1>{randrange(from_, before)}</h1>
                                                <input type="text"
                                                    class="form-control"
                                                    autocomplete="off"
                                                    placeholder="first number"
                                                    name="from"
                                                    value="{from_}">
                                                <input type="text"
                                                    class="form-control"
                                                    autocomplete="off"
                                                    placeholder="second number"
                                                    name="before"
                                                    value="{before}">
                                                <button type="submit" class="btn btn-primary">Generate</button>
                                            </center>
                                        </form>
                                    </body>
                                </html>'''
    elif request.method == 'POST':
        from_ = 1 if not request.form['from'] else int(request.form['from'])
        before = 100 if not request.form['before'] else int(request.form['before'])
        nums.append(from_)
        nums.append(before)
        if 'flask_login.mixins.AnonymousUserMixin' in str(flask_login.current_user):
            return f'''<!DOCTYPE html>
                        <html lang="en">
                            <head>
                                <meta charset="utf-8">
                                <link rel="stylesheet"
                                href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                            </head>
                            
                            <body>
                                <form class="form-group" method="post">
                                    <div class="alert alert-primary" role="alert">
                                        <a href="http://127.0.0.1:8080/login">Войти</a>
                                    </div>
                                    <center>
                                        <h1>{randrange(nums[0], nums[1] + 1)}</h1>
                        
                                        <input type="text"
                                               class="form-control"
                                               autocomplete="off"
                                               placeholder="first number"
                                               name="from"
                                               value="{nums[0]}">
                        
                                        <input type="text"
                                               class="form-control"
                                               autocomplete="off"
                                               placeholder="second number"
                                               name="before"
                                               value="{nums[1]}">
                        
                                        <button type="submit" class="btn btn-primary">Generate</button>
                                    </center>
                                </form>
                            </body>
                        </html>'''
        else:
            return f'''<!DOCTYPE html>
                                    <html lang="en">
                                        <head>
                                            <meta charset="utf-8">
                                            <link rel="stylesheet"
                                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                                        </head>

                                        <body>
                                            <form class="form-group" method="post">
                                                <div class="alert alert-primary" role="alert">
                                                    <h4>{flask_login.current_user.name}</h4>
                                                    <a href="http://127.0.0.1:8080/logout">Выйти</a>
                                                </div>
                                                <center>
                                                    <h1>{randrange(nums[0], nums[1] + 1)}</h1>

                                                    <input type="text"
                                                           class="form-control"
                                                           autocomplete="off"
                                                           placeholder="first number"
                                                           name="from"
                                                           value="{nums[0]}">

                                                    <input type="text"
                                                           class="form-control"
                                                           autocomplete="off"
                                                           placeholder="second number"
                                                           name="before"
                                                           value="{nums[1]}">

                                                    <button type="submit" class="btn btn-primary">Generate</button>
                                                </center>
                                            </form>
                                        </body>
                                    </html>'''


@app.route('/image')
def image():
    return f'''<img src="{url_for('static', filename='map.png')}">'''


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
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


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
