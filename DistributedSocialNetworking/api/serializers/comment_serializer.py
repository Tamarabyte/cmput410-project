from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import User, Comment
from api.serializers import AuthorSerializer, ForeignAuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    """A Serializer for the Comment Model"""
    author = AuthorSerializer(read_only=False)
    foreign_author = ForeignAuthorSerializer(read_only=False, required=False)

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """

        # Get the superclass representation
        ret = super(CommentSerializer, self).to_representation(instance)

        # Pop foreign_author... we don't want to print that
        foreign_author = ret.pop('foreign_author', None)

        # Rename 'foreign_author' to 'author' if needed
        author = ret.get('author', None)
        if author is None:
            ret['author'] = foreign_author

        return ret

    class Meta:
            model = Comment
            fields = ('author', 'comment', 'pubDate', 'guid', 'foreign_author')
