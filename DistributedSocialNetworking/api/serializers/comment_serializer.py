from rest_framework import serializers
from Hindlebook.models import Comment, Node, Author
from api.serializers import AuthorSerializer
from api.serializers.utils import get_author


class CommentSerializer(serializers.ModelSerializer):

    """A Serializer for the Comment Model"""
    author = AuthorSerializer(read_only=False, required=True)
    guid = serializers.CharField(max_length=40, required=True)
    pubDate = serializers.DateTimeField()

    def create(self, validated_data):
        """
        Creates and return a new `Comment` instance, given the validated data.
        """

        # Pop nested relationships, we need to handle them separately
        author_data = validated_data.pop('author', None)
        validated_data['author'] = get_author(author_data.get('uuid'), author_data.get('node'))

        return super(CommentSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        """
        Updates and returns an instance of the `Comment` Model with validated data
        """

        # Pop nested relationships, we need to handle them separately
        author_data = validated_data.pop('author', None)
        pubDate = validated_data.get('pubDate', None)

        # Only Update comments if they are newer
        if pubDate and pubDate > instance.pubDate:
            # Set the author
            validated_data['author'] = get_author(author_data.get('uuid'), author_data.get('node'))
            # Call Super to update the Comment instance
            instance = super(CommentSerializer, self).update(instance, validated_data)

        return instance

    class Meta:
            model = Comment
            fields = ('author', 'comment', 'pubDate', 'guid')
