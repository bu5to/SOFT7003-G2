from base import Base, Session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
    __tablename__ = 'username'
    id = Column(Integer, primary_key = True)
    username = Column(String(20), nullable = False, unique = True)
    password = Column(String(80), nullable = False)
    email = Column(String(30), nullable = False, unique = True)

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
#Creates a SQL table for storing user information