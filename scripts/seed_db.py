from flask_blog import create_app
from flask_blog.database import db
from flask_blog.models import Post, Tag, User


def run():
    app = create_app()
    with app.app_context():
        user = User(username="Tom",password="0000")
        
        first_post = Post(
            title="First Post", content="Content for the first post"
        )
        second_post = Post(
            title="Second Post", content="Content for the second post"
        )

        first_post_tag = Tag(post_id=1,content="first")
        first_post_tag2 = Tag(post_id=1,content="post")
        second_post_tag = Tag(post_id=2,content="second")
        second_post_tag2 = Tag(post_id=2,content="post")
        second_post_tag3 = Tag(post_id=2,content="meow")
       
        db.session.add(user)
        db.session.add(first_post)
        db.session.add(first_post_tag)
        db.session.add(first_post_tag2)
        db.session.add(second_post)
        db.session.add(second_post_tag)
        db.session.add(second_post_tag2)
        db.session.add(second_post_tag3)
        db.session.commit()


if __name__ == "__main__":
    run()
