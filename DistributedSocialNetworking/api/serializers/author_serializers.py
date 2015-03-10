from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import User, ForeignUser


class AuthorSerializer(serializers.ModelSerializer):
    """ Used for sending author JSON data to other nodes """
    displayname = serializers.CharField(source='username')
    host = serializers.CharField(source='node')
    id = serializers.CharField(source='uuid')

    class Meta:
        model = User;
        fields = ["displayname", "host", "id"]

class ForeignAuthorSerializer(serializers.ModelSerializer):
    """ Used for sending/retrieving foreign author JSON data to/from other nodes """
    displayname = serializers.CharField(source='username')
    host = serializers.CharField(source='node')
    id = serializers.CharField(source='uuid')

    class Meta:
        model = ForeignUser;
        fields = ["displayname", "host", "id"]

class UserEditSerializer(serializers.ModelSerializer):
    """ Used locally to allow users to edit their user profile"""

    def update(self, validated_data):
        user = User(
            github_id=validated_data['github_id'],
            avatar=validated_data['avatar'],
            about=validated_data['about']
        )

        user.save()
        return user

    class Meta:
        model = User;
        include = ["uuid", "github_id", "avatar", "about"]
        read_only_fields = ['uuid']


