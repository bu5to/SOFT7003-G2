from flask import Flask, render_template, make_response, send_from_directory, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask.cli import with_appcontext
from forms import RegisterForm, LoginForm
from base import Session, engine, Base
from datetime import datetime
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
import click
import shutil
import sys
import os

#import io
#from io import BytesIO
#from google.cloud import storage
#import shutil
import os
from models import User, Thread, Message

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://jiyerqtkdtzmiq:b0b8a7677c2904fe4e37412e1452190cc4368512c9ad0542071835b7ac713ec3@ec2-54-220-243-77.eu-west-1.compute.amazonaws.com:5432/dbh08b84org3rp'
# Edit to connect to SQL database
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/img/'

# We need to produce an actual secret key, min 30 random characters, min 256 bits.
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# This allows flask to manage the login process, i.e. loading users according to IDs.

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'servicekey_googlecloud.json'
#storage_client = storage.Client()
#bucket = storage_client.get_bucket("dataproc-staging-us-central1-956207202528-venq6ohn")

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


@app.route("/courtplanner")
def about():
    return render_template('courtplanner.html')


@app.route("/trainingplans")
def trainingplans():
    return render_template('about.html')


@app.route("/forum")
def forum():
    threads = Thread.getAllThreads()
    tags = Thread.getAllTags()
    return render_template('forum.html', threads=threads, tags=tags)

@app.route('/thread/<int:thread_id>', methods=["GET", "POST"])
def thread(thread_id):
    session = Session()
    query = session.query(Thread)
    thread = query.filter(Thread.id==thread_id).first()
    messages = Message.get_messages_by_id(thread_id)
    if request.method == 'POST':
        content = request.form['content']
      #  sesMsg = Session()
        user = current_user.name
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        message = Message(user, thread, date_time, content)
        current_db_sessions = Session.object_session(message)
        current_db_sessions.add(message)
        current_db_sessions.commit()
        current_db_sessions.close()

    else:
        return render_template("thread.html", thread = thread, messages = messages)

@app.route("/team")
def team():
    return render_template('team.html')

@app.route("/techniques")
def techniques():
    return render_template('techniques.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/newthread", methods=['GET', 'POST'])
def newthread():
    if request.method == "POST":
        title = request.form['title']
        titleStr = title.replace(" ", "").lower()
        description = request.form['description']
        video = request.form['video']
        video = video.replace("watch?v=", "embed/")
        if 'file' not in request.files:
            print('No file')
        file = request.files.get('file')
        print(file)
        if file.filename == '':
            print("No selected file")
        if file:
            filename = secure_filename(titleStr + ".png")
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            dst = filename
        else:
            dst = ""
        tag = request.form['tags']
        if tag == "newtag":
            tag = request.form['newtagtext'] #If a new tag is created, it will pick up the value from the new tag text field instead.
        #sesThread = Session()
        user = User.get_user(current_user.username)
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        thread = Thread(user,title,description,dst,video,date_time,tag)
        current_db_sessions = Session.object_session(thread)
        current_db_sessions.add(thread)
        current_db_sessions.commit()
        current_db_sessions.close()
    return render_template('newthread.html')

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
        else:
            flash(u'Invalid user or password.', 'error')
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
        session.expunge_all()
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
    #Base.metadata.drop_all(bind=engine, tables=[User.__table__])
    Base.metadata.create_all(engine)
    session = Session()
    #u1 = User("19179422", "Jorge El Busto", "19179422@brookes.ac.uk", "password")
    #session.add(u1)
    session.commit()
    print("Tables have been created.")
    session.close()


if __name__ == '__main__':
    create_tables()
    app.run()
