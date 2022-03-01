from base import Base, Session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    username = Column(String(20), nullable = False, unique = True)
    name = Column(String(30), nullable = False, unique = True)
    email = Column(String(40), nullable=False, unique=True)
    password = Column(String(256), nullable = False)

    def __init__(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def get_users():
        sesUsers = Session()
        users = sesUsers.query(User)
        users = users.all()
        print(users)
        sesUsers.close()
        return users

    def get_user(username):
        users = User.get_users()
        for user in users:
            if user.username == username:
                return user
        return None

    def get_user_by_id(id):
        users = User.get_users()
        for user in users:
            if user.id == id:
                return user
        return None

    def get_user_by_email(email):
        users = User.get_users()
        for user in users:
            if user.email == email:
                return user
        return None

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

#Creates a SQL table for storing user information