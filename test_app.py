import pytest
from wsgi import create_app, app
from contextlib import contextmanager
from models import Thread

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
    strings = [b'input class="form-control" id="username"', b'input class="form-control" id="password"']
    response = client.get("/login")
    for string in strings:
        assert string in response.data

def test_access(client):
    '''
    AC-NB-02.0: Given that I want to access the application,
    when I access the application from my browser,
    then it works without issue.
    '''
    response = client.get("/")
    assert (response.status_code == 200)

def test_sharingDiagram(client):
    '''
    AC-NB-08.1: Given that I have shared the diagram in the forum,
    when other coaches access the forum entry,
    then they can see the diagram along with the text.
    '''
    thread = Thread.getThreadById(4)
    response = client.get("/thread/" + str(thread.id))
    imageName = thread.title.replace(" ", "").lower()
    imageName = bytes(imageName,"utf-8")
    assert (response.status_code == 200 and imageName in response.data)

def test_register(client):
    '''
    AC-NB-10.0: Given that I want to register an account,
    when I access the application,
    there is a register account page, then I can securely create an account using my chosen email and password.
    '''
    strings = [b'input class="form-control" id="email"', b'input class="form-control" id="password"']
    response = client.get("/register")
    for string in strings:
        assert string in response.data

def testTagCategories(client):
    '''
    AC-NB-17.1: Given that I want to easily find the videos I intend to show,
    when I enter the videos page,
    then the videos are clearly named and separated into categories.
    '''
    response = client.get("/forum")
    tags = Thread.getAllTags()
    for tag in tags:
        tag = bytes(tag, 'utf-8')
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