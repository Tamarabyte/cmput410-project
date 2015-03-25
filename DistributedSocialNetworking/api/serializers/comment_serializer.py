from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Comment
from api.serializers import AuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    """A Serializer for the Comment Model"""
    author = AuthorSerializer(read_only=False)

    class Meta:
            model = Comment
            fields = ('author', 'comment', 'pubDate', 'guid')


class NonSavingCommentSerializer(serializers.ModelSerializer):
    """A Serializer for the Comment Model"""
    author = AuthorSerializer(read_only=False)

    def create(self, validated_data):
            author = comment.pop('author', None)
            if author is None:
                raise serializers.ValidationError('The Author field of a Comment is required.')

            author = self.get_author(author)

            return Comment(author=author, **validated_data)

    class Meta:
            model = Comment
            fields = ('author', 'comment', 'pubDate', 'guid')
