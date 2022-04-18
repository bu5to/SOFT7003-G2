from base import Base, Session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    name = Column(String(30), nullable=False, unique=True)
    email = Column(String(40), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    plans = relationship("Plan", lazy='subquery')
    threads = relationship("Thread", lazy='subquery')

    def __init__(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def get_users():
        '''
        An array of the registered users is retrieved in this method.
        :return: The array that contains the information in every user.
        '''
        sesUsers = Session()
        users = sesUsers.query(User)
        users = users.all()
        print(users)
        return users

    def get_user(username):
        '''
        In this method, the data of the user is retrieved given its username.
        :return: The user as an object with all of its details.
        '''
        users = User.get_users()
        for user in users:
            if user.username == username:
                return user
        return None

    def get_user_by_id(id):
        '''
        This method follows the same structure as the one before.
        However, here, the ID is the parameter that will be used to search the user.
        :return: The user as an object with all of its details.
        '''
        users = User.get_users()
        for user in users:
            if user.id == id:
                return user
        return None

    def get_user_by_email(email):
        '''
        This method follows the same structure as the one before.
        However, here, the email is the parameter that will be used to search the user.
        :return: The user as an object with all of its details.
        '''
        users = User.get_users()
        for user in users:
            if user.email == email:
                return user
        return None

    def set_password(self, password):  # A password hash is generated with SHA256 method in order to respect the privacy
        self.password = generate_password_hash(password)

    def check_password(self, password):  # The hash is checked.
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Plan(Base):
    __tablename__ = 'plan'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="plans")
    title = Column(String(30), nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=True)

    def __init__(self, user, title, description, image):
        self.user = user
        self.title = title
        self.description = description
        self.image = image


class Thread(Base):
    __tablename__ = 'thread'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="threads")
    title = Column(String(30), nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=True)
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
        '''
        An array with the tags that will be displayed in the front-end, in the "view threads" section, is retrieved from the DB.
        :return: the array with the tags.
        '''
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
        '''
        An array with the threads is retrieved from the database.
        :return: The array containing all the threads registered in the database.
        '''
        sesThreads = Session()
        sesThreads.expire_on_commit = False
        threads = sesThreads.query(Thread)
        threads = threads.all()
        print(threads)
        return threads

    def getThreadById(id):
        '''
        The thread is searched by its ID.
        :return: the thread as an object, with its essential and optional information.
        '''
        threads = Thread.getAllThreads()
        for thread in threads:
            if thread.id == id:
                return thread
        return None

    def convertToEmbedded(video):
        # The URL of a standard YouTube video is converted to the URL of an embedded YouTube video.
        video = video.replace("watch?v=", "embed/")
        return video


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    thread_id = Column(Integer, ForeignKey('thread.id'), nullable=False)
    thread = relationship("Thread", back_populates="messages")
    date = Column(String, nullable=True)
    content = Column(String, nullable=False)


    def get_messages_by_id(thread_id):
        '''
        When a thread is accessed in the forum, all the comments made in that thread are retrieved as an array.
        :return: The array with the message.
        '''
        sesMsg = Session()
        messages = sesMsg.query(Message).filter(Message.thread_id == thread_id).all()
        sesMsg.close()
        return messages

    def __init__(self, name, thread, date, content):
        self.name = name
        self.thread = thread
        self.date = date
        self.content = content

