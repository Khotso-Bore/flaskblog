import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from flask_blog.views.posts import delete

from . import models, mutations
from .types import PostConnection, TagConnection


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    posts = SQLAlchemyConnectionField(PostConnection)
    postbytag = SQLAlchemyConnectionField(PostConnection,tag=graphene.List(graphene.String))
    postsbydate = SQLAlchemyConnectionField(PostConnection,startdate=graphene.String(required=True),enddate=graphene.String(required=True))
    tags = SQLAlchemyConnectionField(TagConnection)
    

    def resolve_posts(self, info, *args, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Post, info, *args, **kwargs
        )
        print("This is ", query)
        #return query.filter(models.Post.title=="nn2").all()
        #return query.filter(models.Post.id==1).all()
        # tags_query = query.filter(models.Post.id==1).all()
        #print(tags_query)
        
        return query.all()

    def resolve_postbytag(self, info, *args, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Post, info, *args, **kwargs
        )
        tag = kwargs.get("tag")
        return query.filter(models.Tag.content.in_(tag), models.Post.id==models.Tag.post_id).all()
    
    def resolve_postsbydate(self, info, *args, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Post, info, *args, **kwargs
        )

        startdate= kwargs.get("startdate")
        enddate = kwargs.get("enddate")
        return query.filter(models.Post.created_at>=startdate,models.Post.created_at<=enddate).all()
    
    def resolve_tags(self, info, *args, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Tag, info, *args, **kwargs
        )
        return query.all()
    
    

    
class Mutation(graphene.ObjectType):
    create_post = mutations.CreatePost.Field()
    edit_post = mutations.EditPost.Field()
    delete_post = mutations.DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
