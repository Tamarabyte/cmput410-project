from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import User, Comment
from api.serializers import AuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    """A Serializer for the Comment Model"""
    author = AuthorSerializer(read_only=False)

    class Meta:
            model = Comment
            fields = ('author', 'comment', 'pubDate', 'guid')
