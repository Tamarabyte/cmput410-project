from rest_framework import serializers
from Hindlebook.models import Author, Node
from api.serializers import AuthorSerializer, PostSerializer
from api.serializers.utils import get_author
import re


class FriendQuerySerializer(serializers.Serializer):
    """
    Serializer for a Friend Query Object
    """
    query = serializers.CharField(max_length=40, required=True)
    author = serializers.CharField(max_length=40, required=True)
    authors = serializers.ListField(child=serializers.CharField(max_length=40, required=True))

    def validate_query(self, value):
        """
        Check that the friends: query key exists
        """
        if(value != "friends"):
            raise serializers.ValidationError("Missing or invalid 'query: friends'")
        return value

    def validate_authors(self, value):
        """
        Filter out invalid UUIDs and UUIDs that are unknown to us
        """
        authors = []

        for uuid in value:
            if Author.objects.filter(uuid=uuid).first():
                authors.append(uuid)  # This is a valid author
        return authors


class FriendRequestSerializer(serializers.Serializer):
    """
    Serializer for a Friend Request Object
    """
    query = serializers.CharField(max_length=40, required=True)
    author = AuthorSerializer(read_only=False, required=True)
    friend = AuthorSerializer(read_only=False, required=True)

    def validate_query(self, value):
        """
        Check that the friendrequest key exists
        """
        if(value != "friendrequest"):
            raise serializers.ValidationError("Missing or invalid 'query: friendrequest'")
        return value

    def validate_author(self, value):
        return getAuthor(value)

    def validate_friend(self, value):
        return getAuthor(value)
