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
    plans = relationship("Plan")
    threads = relationship("Thread")
    messages = relationship("Message")

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
   #     sesUsers.close()
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

class Plan(Base):
    __tablename__ = 'plan'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    user = relationship("User", back_populates="plans")
    title = Column(String(30), nullable = False)
    description = Column(String, nullable = False)
    image = Column(String, nullable = True)

    def __init__(self, user, title, description, image):
        self.user = user
        self.title = title
        self.description = description
        self.image = image

class Thread(Base):
    __tablename__ = 'thread'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    user = relationship("User", back_populates="threads")
    title = Column(String(30), nullable = False)
    description = Column(String, nullable = False)
    image = Column(String, nullable = True)
    video = Column(String, nullable=True)
    date = Column(String, nullable=True)
    tag = Column(String, nullable=True)
    messages = relationship("Message")

    def __init__(self, user, title, description, image, video, date, tag):
        self.user = user
        self.title = title
        self.description = description
        self.image = image
        self.video = video
        self.date = date
        self.tag = tag

    def getAllTags():
        sesTags = Session()
        sesTags.expire_on_commit = False
        newTags = []
        tags = sesTags.query(Thread.tag).distinct()
        tags = tags.all()
        sesTags.expunge_all()
        sesTags.close()
        for tag in tags:
            newTags.append(tag[0])
        return newTags

    def getAllThreads():
        sesThreads = Session()
        sesThreads.expire_on_commit = False
        threads = sesThreads.query(Thread)
        threads = threads.all()
        print(threads)
        return threads

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    user = relationship("User", back_populates="messages")
    thread_id = Column(Integer, ForeignKey('thread.id'), nullable=False)
    thread = relationship("Thread", back_populates="messages")
    date = Column(String, nullable=True)
    content = Column(String, nullable = False)

    def get_messages_by_id(thread_id):
        sesMsg = Session()
        messages = sesMsg.query(Message).filter(Message.thread_id == thread_id).all()
        sesMsg.expunge_all()
    #    sesMsg.close()
        return messages

    def __init__(self, user, thread, date, content):
        self.user = user
        self.thread = thread
        self.date = date
        self.content = content

#Creates a SQL table for storing user information