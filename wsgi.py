from flask import Flask, render_template, make_response, send_from_directory, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask.cli import with_appcontext
from forms import RegisterForm, LoginForm
from base import Session, engine, Base
import click
from models import User

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://jiyerqtkdtzmiq:b0b8a7677c2904fe4e37412e1452190cc4368512c9ad0542071835b7ac713ec3@ec2-54-220-243-77.eu-west-1.compute.amazonaws.com:5432/dbh08b84org3rp'
# Edit to connect to SQL database
app.config['SECRET_KEY'] = 'thisisasecretkey'
# We need to produce an actual secret key, min 30 random characters, min 256 bits.
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# This allows flask to manage the login process, i.e. loading users according to IDs.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template(
        'index.html')  # now, when entering 127.0.0.0:5000/, the file index.html will pop up in the browser.


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
    form = LoginForm()
    if form.validate_on_submit():
        if form.data['submit']:
            print("It works")
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    session = Session()
    if form.validate_on_submit():
        print("It works")
        if form.data['submit']:
            new_user = User(username=form.username.data, password=hashed_password, email=form.email.data)
            session.add(new_user)
            session.commit()
            return redirect(url_for('login'))
    return render_template('/register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for='/login')


# @click.command()
# @with_appcontext
def create_tables():
    Base.metadata.drop_all(bind=engine, tables=[User.__table__])
    Base.metadata.create_all(engine)
    session = Session()
    u1 = User("1", "SampleText", "testuser@brookes.ac.uk", "password")
    session.add(u1)
    session.commit()
    print("Tables have been created.")
    session.close()


if __name__ == '__main__':
    create_tables()
    app.run(debug == True)
