from flask import Flask, render_template, make_response, send_from_directory, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms import RegisterForm, LoginForm
from base import Session, engine, Base
from datetime import datetime
from werkzeug.utils import secure_filename
from models import User, Thread, Message


def create_app():
    '''
    This method creates the application and sets up some environment variables that will need to be accessed
    later.
    :return: The created application.
    '''
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://jiyerqtkdtzmiq:b0b8a7677c2904fe4e37412e1452190cc4368512c9ad0542071835b7ac713ec3@ec2-54-220-243-77.eu-west-1.compute.amazonaws.com:5432/dbh08b84org3rp'
    # Edit to connect to SQL database
    app.config['SECRET_KEY'] = 'thisisasecretkey'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/img/'
    return app


app = create_app()
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    '''
    Implementation of LoginManager in Flask.
    :param user_id: the ID of the user that will be logging in
    :return: The user as an object, with his/her detailed information.
    '''
    users = User.get_users()
    for user in users:
        if user.id == int(user_id):
            return user
    return None


@app.route("/")
def index():
    '''
    The home page of the project. If the user has been authenticated,
    the tabs with the features will be displayed. If not, the user will only have
    the "log in" and "register" options, apart from the home page.
    :return: The Index.html template, which consists of the "home" page of the project.
    '''
    if current_user.is_authenticated:
        user = User.get_user(current_user.username)
    else:
        user = None
    return render_template(
        'index.html', user=user)


@app.route("/courtplanner")
def about():
    '''
    This URL belongs to the court planner, where tactics can be drawn.
    :return: The court planner page.
    '''
    return render_template('courtplanner.html')


@app.route("/trainingplans")
def trainingplans():
    '''
    This URL belongs to the training plans section, where tactics can be drawn.
    :return: The training plans page.
    '''
    return render_template('about.html')


@app.route("/forum")
def forum():
    '''
    Before accessing the forum, all the threads and all the tags are displayed, to
    sort the threads by tabs accordingly later on.
    :return:
    '''
    threads = Thread.getAllThreads()
    tags = Thread.getAllTags()
    return render_template('forum.html', threads=threads, tags=tags)


@app.route('/thread/<int:thread_id>', methods=["GET", "POST"])
def thread(thread_id):
    '''
    This is a dynamic URL that will lead to a thread, according to its ID.
    If the request is POST, it means that someone is clicking on the "Reply" button.
    Therefore, the comment will be added.
    :param thread_id: The ID of the thread whose content is meant to be displayed.
    :return: The thread template.
    '''
    session = Session()
    query = session.query(Thread)
    thread = query.filter(Thread.id == thread_id).first()
    messages = Message.get_messages_by_id(thread_id)
    if request.method == 'POST':
        content = request.form['content']
        user = current_user.name
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        message = Message(user, thread, date_time, content)
        current_db_sessions = Session.object_session(message)
        current_db_sessions.add(message)
        current_db_sessions.commit()
        current_db_sessions.close()

    else:
        return render_template("thread.html", thread=thread, messages=messages)


@app.route("/team")
def team():
    return render_template('team.html')


# Common drills and techniques.
@app.route("/techniques")
def techniques():
    '''
    In this webpage, common drills and techniques are displayed.
    :return: techniques.html
    '''
    return render_template('techniques.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/newthread", methods=['GET', 'POST'])
def newthread():
    '''
    URL to post new threads to the forum. Code is explained step by step below,
    as there are many key features that are considered in this request.
    :return: The thread posting form.
    '''
    if request.method == "POST":
        # The attributes from the form are picked up and a new thread is added to the database.
        title = request.form['title']
        titleStr = title.replace(" ", "").lower()
        description = request.form['description']
        video = request.form['video']
        video = Thread.convertToEmbedded(video)
        # Here, the file retrieved from the file chooser is copied to the static folder of the project.
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
            tag = request.form[
                'newtagtext']  # If a new tag is created, it will pick up the value from the new tag text field instead.
        # sesThread = Session()
        user = User.get_user(current_user.username)
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        thread = Thread(user, title, description, dst, video, date_time, tag)
        current_db_sessions = Session.object_session(thread)
        current_db_sessions.add(thread)
        current_db_sessions.commit()
        current_db_sessions.close()
    return render_template('newthread.html')


@app.route('/sw.js')
def sw():
    '''
    Implementation of the service worker in JavaScript.
    :return: The content of the service worker as a response.
    '''
    response = make_response(
        send_from_directory('static', path='sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Method to log in. Below, the encrypted password is checked and it is also checked whether the username and password
    are right before logging in.
    Note that the password is not saved as raw text in the database. It gets encrypted before being stored.
    :return: The login form.
    '''
    if current_user.is_authenticated:  # This method is implemented by the Flask library itself.
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
    '''
    The user will be registered if there is a POST request
    :return:
    '''
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
    '''
    The user is logged out.
    :return: Login webpage.
    '''
    logout_user()
    return redirect(url_for('login'))


def create_tables():
    '''
    Method to create the tables in the PostgreSQL database with the SQLAlchemy library.
    '''
    Base.metadata.create_all(engine)
    print("Tables have been created.")


if __name__ == '__main__':
    create_tables()
    app.run()
