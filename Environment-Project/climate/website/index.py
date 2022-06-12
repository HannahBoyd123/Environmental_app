from flask import render_template, Blueprint, session

index = Blueprint('index', __name__,)

@index.route('/')
def home():
    user_logged_in = 'id' in session
    return render_template('home.html', user_logged_in=user_logged_in)

@index.route('/home')
def backHome():
    user_logged_in = 'id' in session
    return render_template('home.html', user_logged_in=user_logged_in)

@index.route('/aboutus')
def aboutUs():
    user_logged_in = 'id' in session
    return render_template('aboutus.html', user_logged_in=user_logged_in)

@index.route('/history')
def history():
    user_logged_in = 'id' in session
    return render_template('history.html', user_logged_in=user_logged_in)


@index.route('/base')
def base():
    user_logged_in = 'id' in session
    return render_template('base.html', user_logged_in=user_logged_in)

@index.route('/index')
def index1():
    user_logged_in = 'id' in session
    return render_template('index.html', user_logged_in=user_logged_in)

@index.route('/map')
def map():
    user_logged_in = 'id' in session
    return render_template('map.html', user_logged_in=user_logged_in)

@index.route("/FAQ.html")
def faq():
    user_logged_in = 'id' in session
    return render_template('FAQ.html', user_logged_in=user_logged_in)