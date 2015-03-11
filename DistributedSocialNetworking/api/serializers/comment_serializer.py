from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Post, User, Comment
from api.serializers import AuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    """A Serializer for the Comment Model"""
    author = AuthorSerializer(read_only=True)

    def create(self, validated_data):
        """Create and return a new `Comment` instance, given the validated data."""

        # TODO: What to do with author data??
        # If not our host, add as foreign???
        # If our host but unseen, add a new user??? Or reject as invalid??
        author_data = validated_data.pop('author')

        # # Create the comments
        # comment_data = validated_data.pop('comments')
        # Comment.objects.create(**comment_data)

        return super(CommentSerializer, self).update(validated_data)

    class Meta:
            model = Comment
            fields = ('author', 'comment', 'pubDate', 'guid')
