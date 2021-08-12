import graphene
from graphene import relay
from graphene.types.scalars import String
from six import print_

from flask_blog.views.posts import delete

from .. import models, types
from ..database import db


class CreatePostInput:
    title = graphene.String(required=True)
    content = graphene.String(required=True)


class CreatePostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class CreatePostOutput(graphene.Union):
    class Meta:
        types = (CreatePostSuccess,)


class CreatePost(relay.ClientIDMutation):
    Input = CreatePostInput
    Output = CreatePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        new_post = models.Post(**input)

        db.session.add(new_post)
        db.session.commit()

        return CreatePostSuccess(post=new_post)

class EditPostInput:
    id = graphene.Int(required=True)
    title = graphene.String(required=False)
    content = graphene.String(required=False)


class EditPostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class EditPostOutput(graphene.Union):
    class Meta:
        types = (EditPostSuccess,)


class EditPost(relay.ClientIDMutation):
    Input = EditPostInput
    Output = EditPostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        post_id = input.get("id")
        edit_post = models.Post.query.get(post_id)
        
        if(input.get("title")):
            edit_post.title = input.get("title")
        
        if(input.get("content")):
            edit_post.content = input.get("content")

        db.session.commit()

        return EditPostSuccess(post=edit_post)

class DeletePostInput:
    id = graphene.Int(required=True)


class DeletePostSuccess(graphene.ObjectType):
    post = graphene.String(required=True)



class DeletePostOutput(graphene.Union):
    class Meta:
        types = (DeletePostSuccess,)


class DeletePost(relay.ClientIDMutation):
    Input = DeletePostInput
    Output = DeletePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        post_id = input.get("id")
        delete_post = models.Post.query.get(post_id)
        models.Tag.query.filter(models.Tag.post_id==post_id).delete(synchronize_session=False)
        db.session.delete(delete_post)
        db.session.commit()

        return DeletePostSuccess(post="deleted")
