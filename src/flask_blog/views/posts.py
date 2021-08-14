from flask import Blueprint, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

from ..database import db
from ..models import Post, Tag, User
from ..loginmanager import lm
from datetime import datetime
from sqlalchemy import func
from flask_login import login_user, login_required, logout_user

posts = Blueprint("posts", __name__)


@posts.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@posts.route("/<int:post_id>")
def post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    return render_template("post.html", post=post)


@posts.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            new_post = Post(title=title, content=content)

            db.session.add(new_post)
            db.session.flush()

            new_tag = Tag(post_id=new_post.id, content="hello")
            db.session.add(new_tag)
            db.session.commit()

            return redirect(url_for("posts.index"))
    return render_template("create.html")


@posts.route("/<int:post_id>/edit", methods=("GET", "POST"))
def edit(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            post.title = title
            post.content = content

            db.session.commit()

            return redirect(url_for("posts.index"))

    return render_template("edit.html", post=post)


@posts.route("/<int:post_id>/delete", methods=("POST",))
def delete(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    db.session.delete(post)
    db.session.commit()

    flash('"{}" was successfully deleted!'.format(post.id))
    return redirect(url_for("posts.index"))


@posts.route("/fil", methods=("POST",))
def fil():
    if request.method == "POST":
        tag = request.form["tag"]

        posts = Post.query.filter(
            Tag.content == tag, Post.id == Tag.post_id
        ).all()
        return render_template("index.html", posts=posts)
    return render_template("index.html", posts=[])


@posts.route("/date", methods=("GET", "POST"))
def date():
    if request.method == "POST":
        date = request.form["date"]

        posts = Post.query.filter(
            func.date(Post.created_at)
            == datetime.strptime(date, "%Y-%m-%d").date()
        ).all()
        return render_template("index.html", posts=posts)
    return render_template("index.html", posts=[])


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@posts.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter(
            User.username == username, User.password == password
        ).first()

        if user:
            login_user(user)
            return redirect("/loggedin")
        return "who are you?"
    return render_template("index.html", posts=[])


@posts.route("/loggedin")
@login_required
def loggedin():
    return "You are logged in"


@posts.route("/loggout")
@login_required
def logout():
    logout_user()
    return render_template("You are logged out!")
