import flask

from flask_blog import models
from flask_blog.database import db
from datetime import datetime

NO_POSTS_MESSAGE = b"No posts here so far."


def test_empty_db(client):
    rv = client.get("/")
    assert NO_POSTS_MESSAGE in rv.data


def test_create_post(app_context, client):
    title = "Test Post"
    content = "This is a test"
    rv = client.post(
        "/create",
        data=dict(title=title, content=content),
        follow_redirects=True,
    )
    assert flask.request.path == "/"
    assert NO_POSTS_MESSAGE not in rv.data
    assert title.encode() in rv.data

    posts = models.Post.query.all()
    assert len(posts) == 1
    assert posts[0].title == title
    assert posts[0].content == content


def test_edit_post(app_context, client):
    post = models.Post(title="Test Post", content="This is a test")

    db.session.add(post)
    db.session.commit()

    client.post(
        f"{post.id}/edit",
        data=dict(title="New Title", content="New content"),
        follow_redirects=True,
    )

    posts = models.Post.query.all()
    assert len(posts) == 1
    assert posts[0].title == "New Title"
    assert posts[0].content == "New content"


def test_delete_post(app_context, client):
    post = models.Post(title="Test Post", content="This is a test")

    db.session.add(post)
    db.session.commit()

    client.post(
        f"{post.id}/delete",
        data=dict(),
        follow_redirects=True,
    )

    posts = models.Post.query.all()
    assert len(posts) == 0

def test_filter_post_by_tag(app_context, client):
    post = models.Post(title="FirstPost", content="This is a test")
    post2 = models.Post(title="SecondPost", content="This is a test")
    tag = models.Tag(post_id=1, content="post")
    tag2 = models.Tag(post_id=2, content="post")
    tag3 = models.Tag(post_id=2, content="post2")

    db.session.add(post)
    db.session.add(post2)
    db.session.add(tag)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.commit()

    resp = client.post(
        f"/fil",
        data=dict(tag="post"),
        follow_redirects=True,
    )

    assert b"FirstPost" in resp.data
    assert b"SecondPost" in resp.data

    resp2 = client.post(
        f"/fil",
        data=dict(tag="post2"),
        follow_redirects=True,
    )


    assert b"FirstPost" not in resp2.data
    assert b"SecondPost" in resp2.data

def test_filter_post_by_date(app_context, client):
    post = models.Post(title="Test Post", content="This is a test")
    date = datetime.today().date()
    
    db.session.add(post)
    db.session.commit()

    resp = client.post(
        f"/date",
        data=dict(date=str(date)),
        follow_redirects=True,
    )

    assert b"Test Post" in resp.data
    posts = models.Post.query.all()
    assert len(posts) == 1
    assert posts[0].created_at.date() == date
    