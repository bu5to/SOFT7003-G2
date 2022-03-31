import pytest
from wsgi import app
from contextlib import contextmanager
import json
import os
from models import Thread,Message,User,Plan

@pytest.fixture(scope='module')
def test_client():
    flask_app = app

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

#AC-NB-27.0 - The YouTube video that has been input in the upload form is converted to an embedded video.
def test_parseEmbeddedVideos():
    oldVideo = "https://www.youtube.com/watch?v=aBuxsRnU50A"
    oldVideo = Thread.convertToEmbedded(oldVideo)
    embeddedVid = '<iframe width="560" height="315" src="https://www.youtube.com/embed/aBuxsRnU50A" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    assert oldVideo in embeddedVid
