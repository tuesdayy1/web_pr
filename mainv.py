from flask import Flask, request, url_for, render_template, redirect
from random import randrange
from data import db_session
from data.users import User
from forms.user import RegisterForm
import os


app = Flask(__name__, template_folder='templates')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['POST', 'GET'])
def main():
    nums = []
    if request.method == 'GET':
        from_ = 1
        before = 100
        return render_template('index.html', params={'result': randrange(from_, before), })
    elif request.method == 'POST':
        from_ = 1 if not request.form['from'] else int(request.form['from'])
        before = 100 if not request.form['before'] else int(request.form['before'])
        nums.append(from_)
        nums.append(before)
        # return render_template('index.html', params={'result': randrange(from_, before)})
        return f'''<!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                        </head>
                        
                        <body>
                            <center>
                                <form class="form-group" method="post">
                                    <div class="alert alert-primary" role="alert"></div>
                                    <h1>{randrange(nums[0], nums[1])}</h1>
                    
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
                                </form>
                            </center>
                        </body>
                    </html>'''


@app.route('/a', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return f'''
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}"/>
                            <title>Покупка</title>
                          </head>
                          
                          <body>
                            <h1>Форма для регистрации в суперсекретной системе</h1>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <input type="password" class="form-control" id="password" placeholder="Введите пароль" name="password">
                                    <div class="form-group">
                                        <label for="classSelect">В каком вы классе</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>7</option>
                                          <option>8</option>
                                          <option>9</option>
                                          <option>10</option>
                                          <option>11</option>
                                        </select>
                                     </div>
                                    <div class="form-group">
                                        <label for="about">Немного о себе</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готов быть добровольцем</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        print(request.form['class'])
        print(request.form['file'])
        print(request.form['about'])
        print(request.form['accept'])
        print(request.form['sex'])
        return "Форма отправлена"


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


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
