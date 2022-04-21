from flask import Flask, request, url_for, render_template
from random import randrange


app = Flask(__name__)


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
                                <form class="login_form" method="post">
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
                    
                                    <button type="submit" class="btn btn-primary">Write</button>
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')