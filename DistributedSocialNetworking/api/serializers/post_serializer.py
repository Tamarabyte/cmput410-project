from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Post, User, Comment
from api.serializers.comment_serializer import CommentSerializer
from api.serializers.author_serializers import AuthorSerializer


class PostSerializer(serializers.ModelSerializer):
    """A Serializer for the Post Model"""
    author = AuthorSerializer(read_only=False)
    comments = CommentSerializer(many=True, read_only=False)

    def create(self, validated_data):
        """Create and return a new `Post` instance, given the validated data."""

        # TODO: What to do with author data??
        # If not our host, add as foreign???
        # If our host but unseen, add a new user??? Or reject as invalid??
        author_data = validated_data.pop('author')
        comment_data = validated_data.pop('comments')

        #TODO: Fix me
        user = None

        # Create the post
        post = Post.objects.create(user=user)

        # Create the comments
        Comments.objects.create(user=user, post=post, **comment_data)

        return post


    def update(self, validated_data):
        post = Post( )

        post.save()
        return post

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'content_type', 'content', 'author', 'categories',
                  'comments', 'pubDate', 'guid', 'visibility')
