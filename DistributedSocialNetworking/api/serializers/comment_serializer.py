from rest_framework import serializers
from Hindlebook.models import Comment
from api.serializers import AuthorSerializer


class CommentSerializer(serializers.ModelSerializer):

    """A Serializer for the Comment Model"""
    author = AuthorSerializer(read_only=False)
    guid = serializers.CharField(max_length=40, required=True)
    pubDate = serializers.DateTimeField()

    class Meta:
            model = Comment
            fields = ('author', 'comment', 'pubDate', 'guid')
