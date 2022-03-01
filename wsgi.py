from flask import Flask, render_template, make_response, send_from_directory, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask.cli import with_appcontext
from forms import RegisterForm, LoginForm
from base import Session, engine, Base
from werkzeug.urls import url_parse
import click
import sys
from models import User

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://jiyerqtkdtzmiq:b0b8a7677c2904fe4e37412e1452190cc4368512c9ad0542071835b7ac713ec3@ec2-54-220-243-77.eu-west-1.compute.amazonaws.com:5432/dbh08b84org3rp'
# Edit to connect to SQL database
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# We need to produce an actual secret key, min 30 random characters, min 256 bits.
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# This allows flask to manage the login process, i.e. loading users according to IDs.

@login_manager.user_loader
def load_user(user_id):
    users = User.get_users()
    for user in users:
        if user.id == int(user_id):
            return user
    return None


@app.route("/")
def index():
    if current_user.is_authenticated:
        user = User.get_user(current_user.username)
    else:
        user = None
    return render_template(
        'index.html', user=user)  # now, when entering 127.0.0.0:5000/, the file index.html will pop up in the browser.


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/services")
def services():
    return render_template('services.html')


@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')


@app.route("/team")
def team():
    return render_template('team.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route('/sw.js')
def sw():
    response = make_response(
        send_from_directory('static', path='sw.js'))
    # change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response


# These URLs above will be later on substituted by the sections specified
# in the document.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('index.html')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    session = Session()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data, email=form.email.data,
                        name=form.name.data)
        session.add(new_user)
        session.commit()
        session.close()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# @click.command()
# @with_appcontext
def create_tables():
    Base.metadata.drop_all(bind=engine, tables=[User.__table__])
    Base.metadata.create_all(engine)
    session = Session()
    u1 = User("19179422", "Jorge El Busto", "19179422@brookes.ac.uk", "password")
    session.add(u1)
    session.commit()
    print("Tables have been created.")
    session.close()


if __name__ == '__main__':
    create_tables()
    app.run(debug == True)
