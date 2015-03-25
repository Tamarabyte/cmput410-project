from rest_framework import serializers
from Hindlebook.models import Author, Node
from api.serializers import AuthorSerializer
import re


class FriendQuerySerializer(serializers.Serializer):
    """
    Serializer for a Friend Query Object
    """
    query = serializers.CharField(max_length=40, required=True)
    author = serializers.CharField(max_length=40, required=True)
    authors = serializers.ListField(child=serializers.CharField(max_length=40, required=True))

    def uuid_validator(self, value):
        """
        Validates a UUID
        """
        regex = re.compile('^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')
        match = regex.match(value)
        return bool(match)

    def validate_query(self, value):
        """
        Check that the friends: query key exists
        """
        if(value != "friends"):
            raise serializers.ValidationError("Missing or invalid 'query: friends'")
        return value

    def validate_author(self, value):
        """
        Check that the author is a valid UUID
        """
        if self.uuid_validator(value) is False:
            raise serializers.ValidationError("Author UUID is invalid")
        return value

    def validate_authors(self, value):
        """
        Filter out invalid UUIDs and UUIDs that are unknown to us
        """
        authors = []

        for uuid in value:
            if self.uuid_validator(uuid) is False:
                continue  # Bad UUID, skip it
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

    def author_validator(self, value):
        """
        A Validator for the Author/Friend fields of a friend request
        """
        username = value.get('username')
        uuid = value.get('uuid')
        node = value.get('node')

        # Reject unknown hosts
        node = Node.objects.filter(host=node).first()
        if node is None:
            raise serializers.ValidationError("Invalid or unknown Host: %s" % node)

        # Get or create Author
        author = Author.objects.filter(uuid=uuid).first()
        if author is None:
            # TODO FIX ME: Insert Foreign Author Profile Grab
            author = Author.objects.create(username=username, uuid=uuid, node=node)
        # elif author.user is None:
            # TODO: FIX ME: Insert Foreign Author Profile Update

        return author

    def validate_author(self, value):
        return self.author_validator(value)

    def validate_friend(self, value):
        return self.author_validator(value)
