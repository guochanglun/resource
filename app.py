from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta
from model.User import User
from model.Resource import Resource
from functools import wraps
import json


# 控制登录检测
def require_login(func):
    @wraps(func)
    def require_login_call():
        if 'userid' not in session.keys():
            return redirect(url_for('index'))
        return func()
    return require_login_call


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.secret_key = 'gcl110110'


@app.route('/')
def index():
    # if user already login, redirect to search
    if 'userid' in session.keys():
        return redirect(url_for('search'))
    return render_template('login.html')


@app.route('/index')
def index2():
    return index()


@app.route('/login')
def login():
    return index()


@app.route('/logout')
def logout():
    if session['userid'] is not None:
        del session['userid']
    return redirect(url_for('index'))


@app.route('/login.do', methods=['post'])
def login_do():
    username = request.form.get('username')
    password = request.form.get('password')
    users = User.select().where(User.username == username, User.password==password)
    if len(users) != 0:
        if users[0].password == password:
            # login success
            session['userid'] = users[0].get_id()
            return redirect(url_for('search'))
    return render_template("login.html")


@app.route('/search')
@require_login
def search():
    return render_template('index.html')


@app.route('/search.do', methods=['post'])
@require_login
def search_do():
    content = request.form.get('content')
    res = Resource.select().where(Resource.title.contains(content))
    return render_template('list.html', res=res)


@app.route('/edit')
@require_login
def edit():
    return render_template('edit.html')


@app.route('/edit.do', methods=['post'])
@require_login
def edit_do():
    title = request.form.get('title')
    markdown = request.form.get('markdown')
    html = request.form.get('html')
    # save resource
    res = Resource(title=title, markdown=markdown, html=html)
    res.save()
    return json.dumps({'msg': 'success'}, ensure_ascii=False)


@app.route('/mine')
@require_login
def mine():
    userid = session.get('userid')
    user = User.get_by_id(userid)
    return render_template('mine.html', user=user)


@app.route('/mine.do', methods=['post'])
@require_login
def mine_do():
    userid = session.get('userid')
    user = User.get_by_id(userid)
    username = request.form.get('username')
    password = request.form.get('password')
    desc = request.form.get('desc')
    user.username = username
    user.password = password
    user.desc = desc
    user.save()
    return redirect(url_for('search'))


@app.route('/list')
@require_login
def list():
    return render_template('list.html')


@app.route('/saved')
@require_login
def saved():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
