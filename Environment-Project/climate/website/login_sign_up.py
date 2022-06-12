from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from flask_bcrypt import Bcrypt
from connect_to_db import _connect_to_db
from pollution_and_weather_links import return_user_searches


login_sign_up = Blueprint('login_sign_up', __name__)

login_sign_up.secret_key = '&Potato98&'

# login


@login_sign_up.route('/login', methods=['GET', 'POST'])
def login():
    user_logged_in = 'id' in session
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_id = email_password_exists(email, password)
        if user_id != None:
            session['id'] = user_id[0]
            firstname = user_id[1]
            flash('Successfully logged in!', category='info')
            flash(f'Welcome back {firstname}', category='info')
            return redirect(url_for('login_sign_up.logged_in'))
        else:
            flash('Incorrect username or password, please try again.', category='error')
            flash('Alternatively please create an account using sign up link above', category='error')
            return render_template('login.html')
    if 'id' in session:
        redirect(url_for('login_sign_up.logged_in'))
    else:
        return render_template('login.html', user_logged_in=user_logged_in)
    return render_template('login.html', user_logged_in=user_logged_in)


@login_sign_up.route('/logged_in', methods=['GET', 'POST'])
def logged_in():
    if 'id' in session:
        log = 'log result'
        sessionid = session['id']
        info = return_user_searches(sessionid)
        return render_template('logged_in.html', info=info, data=None, log=log)
    else:
        flash('please login')
        return redirect(url_for("login_sign_up.login"))


@login_sign_up.route("/logout")
def logout():
    session.pop("id", None)
    flash('logged out')
    return redirect(url_for("login_sign_up.login"))


def email_password_exists(email, password):
    connected = _connect_to_db('user_login_details')
    cursor = connected.cursor()
    cursor.execute("SELECT ID, First_Name, password from user_account WHERE email = %s", (email,))
    id_num = None
    name = None
    pw_hash = None
    for (ID) in cursor:
        id_num = ID[0]
        name = ID[1]
        pw_hash = ID[2]
    if id_num != None:
        if Bcrypt().check_password_hash(pw_hash, password):
                name_id = [id_num, name]
                cursor.close()
                connected.close()
                return name_id
        else:
            return None
    else:
        return None

#sign up

@login_sign_up.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    user_logged_in = 'id' in session

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = check_email(email)

        if user is not None:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            insert_user_into_db(first_name, password2, email)
            success="success"
            flash('your account has been created - please login')
            return redirect(url_for('login_sign_up.login')), success

    return render_template('sign_up.html', user_logged_in=user_logged_in)

#functions which connect to the database

def insert_user_into_db(name, password, email):
    connected = _connect_to_db('user_login_details')
    cursor = connected.cursor()
    password = Bcrypt().generate_password_hash(password)
    query = "INSERT INTO user_account(id, First_Name, password, email) VALUES(NULL, %s, %s, %s)"
    cursor.execute(query, (name, password, email))
    connected.commit()
    cursor.close()
    connected.close()


def check_email(email):
    connected = _connect_to_db('user_login_details')
    cursor = connected.cursor()
    cursor.execute("SELECT ID from user_account WHERE email = %s", (email,))
    id_num = None
    for (ID) in cursor:
        id_num = ID
    cursor.close()
    connected.close()
    return id_num