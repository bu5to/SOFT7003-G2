import pytest
from wsgi import create_app, app
from contextlib import contextmanager
import json
import os
from models import Thread,Message,User,Plan
import requests #Cambiar los gets y los posts
from flask import url_for, Flask

@pytest.fixture
def client():
    client = app.test_client()
    return client

def test_login(client):
    '''
        AC-NB-01.0 - Given that I want to log in,
        when I start the application
        there is a log in page then I am able to enter my log in details.
    '''
    response = client.get("/login")
    assert b"login" in response.data

def test_access(client):
    '''
    AC-NB-02.0: Given that I want to access the application,
    when I access the application from my browser,
    then it works without issue.
    '''
   # client = create_app().test_client()
    response = client.get("/")
    assert (response.status_code == 200)

def test_sharingDiagram(client):
    '''
    AC-NB-08.1: Given that I have shared the diagram in the forum,
    when other coaches access the forum entry,
    then they can see the diagram along with the text.
    '''
    client = create_app().test_client()
    thread = Thread.getThreadById(3)
    response = client.get("/thread/" + str(thread.id))
    imageName = thread.title.replace(" ", "").lower()
    assert (response.status_code == 200 and imageName in response)

def test_register():
    '''
    AC-NB-10.0: Given that I want to register an account,
    when I access the application,
    there is a register account page, then I can securely create an account using my chosen email and password.
    '''
    client = create_app().test_client()
    response = client.get("/register")
    assert b"register.html" in response.data

def testTagCategories():
    '''
    AC-NB-17.1: Given that I want to easily find the videos I intend to show,
    when I enter the videos page,
    then the videos are clearly named and separated into categories.
    '''
    client = create_app().test_client()
    response = client.get("/forum")
    tags = Thread.getAllTags()
    for tag in tags:
        assert tag in response.data

def test_parseEmbeddedVideos():
    '''
    AC-NB-25.0: Given that I want to upload a video to the forum,
    when I enter the YouTube URL,
    the embedded video is displayed accordingly in the thread.
    '''
    client = create_app().test_client()
    oldVideo = "https://www.youtube.com/watch?v=aBuxsRnU50A"
    newVideo = Thread.convertToEmbedded(oldVideo)
    embeddedVid = '<iframe width="560" height="315" src="https://www.youtube.com/embed/aBuxsRnU50A" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    assert newVideo in embeddedVid

if __name__ == '__main__':
    pytest.main()