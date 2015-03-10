from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Post, User, Comment
from api.serializers.comment_serializer import CommentSerializer
from api.serializers.author_serializers import AuthorSerializer


class PostSerializer(serializers.ModelSerializer):
    # Default, I think
    # author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), read_only=False)
    author = AuthorSerializer(read_only=False)

    # comments = serializers.StringRelatedField(many=True, allow_null=True, read_only=False)

    comments = CommentSerializer(many=True, read_only=False)

    class Meta:
        model = Post
        # depth = 1  # Fix to use Author serializer

        fields = ('title', 'source', 'origin', 'description', 'content_type', 'content', 'author', 'categories',
                  'comments', 'pubDate', 'guid', 'visibility')
