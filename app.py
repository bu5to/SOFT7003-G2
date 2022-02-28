from flask import Flask, render_template, make_response, send_from_directory, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'database.db'
#Edit to connect to SQL database
app.config['SECRET_KEY'] = 'thisisasecretkey'
#We need to produce an actual secret key, min 30 random characters, min 256 bits.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
#This allows flask to manage the login process, i.e. loading users according to IDs.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(30), nullable = False, unique = True)
#Creates a SQL table for storing user information

class registerForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min = 5, max = 20)], render_kw={"placeholder": "Password"})
    email = StringField(validators = [InputRequired(), Length(min = 4, max = 30)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Register")
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username has already been taken, please choose a different one.")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("An account using that email already exists.")
#This creates the registry form which can be displayed within the register page.
#If the username or email are already within the database, then it doesn't allow the details to be registered.

class loginForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min = 5, max = 20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

@app.route("/")
def index():
    return render_template('index.html') #now, when entering 127.0.0.0:5000/, the file index.html will pop up in the browser.

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
    response=make_response(
                     send_from_directory('static',path='sw.js'))
    #change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response
#These URLs above will be later on substituted by the sections specified
#in the document.

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username = form.username.data, password = hashed_password, email = form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('/register.html', form = form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for='/login')





            #This is a test comment.