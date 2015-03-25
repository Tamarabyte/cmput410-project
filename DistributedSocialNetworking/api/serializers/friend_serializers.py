from rest_framework import serializers
import re

# class AuthorIDSerializer(serializers.Serializer):
#     author =


class FriendQuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=7, required=True)
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
        Check that the authors contains valid UUID
        """
        for v in value:
            if self.uuid_validator(v) is False:
                raise serializers.ValidationError("At least one of the Authors UUID are invalid")

        return value

    # def save(self):
    #     email = self.validated_data['email']
    #     message = self.validated_data['message']
    #     send_email(from=email, message=message)
