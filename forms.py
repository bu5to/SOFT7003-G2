from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from models import User

class RegisterForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "Username"})
    name = StringField(validators = [InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "Name and surname"})
    password = PasswordField(validators = [InputRequired(), Length(min = 5, max = 20)], render_kw={"placeholder": "Password"})
 #   role = SelectField(u'Role', choices=[('coach', 'Coach'), ('player', 'Player')])
    email = StringField(validators = [InputRequired(), Length(min = 4, max = 30)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Register")
    def validate_username(self, username):
        existing_user_username = User.get_user(username)
        if existing_user_username:
            raise ValidationError("That username has already been taken, please choose a different one.")

    def validate_email(self, email):
        existing_user_email = User.get_user_by_email(email)
        if existing_user_email:
            raise ValidationError("An account using that email already exists.")
#This creates the registry form which can be displayed within the register page.
#If the username or email are already within the database, then it doesn't allow the details to be registered.

class LoginForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min = 5, max = 20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")