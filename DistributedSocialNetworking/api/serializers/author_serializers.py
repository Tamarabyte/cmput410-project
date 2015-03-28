from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    """ Used for sending author JSON data to other nodes """
    displayname = serializers.CharField(source='username')
    host = serializers.CharField(source='node')
    id = serializers.CharField(source='uuid')

    class Meta:
        model = Author
        fields = ["displayname", "host", "id"]


class ProfileSerializer(serializers.ModelSerializer):
    """ Used for sending author JSON data to other nodes """
    displayname = serializers.CharField(source='username')
    host = serializers.CharField(source='node.host')
    id = serializers.CharField(source='uuid')
    friends = AuthorSerializer(many=True)
    github_username = serializers.SerializerMethodField(source='github_id')
    bio = serializers.SerializerMethodField(source='about')

    # Optional field, specify default
    def get_github_username(self, obj):
        return getattr(obj, 'github_username', Author._meta.get_field('github_id').get_default())

    # Optional field, specify default
    def get_bio(self, obj):
        return getattr(obj, 'bio', Author._meta.get_field('about').get_default())

    def create(self, validated_data):
        """
        Creates and return a new `Profile` instance, given the validated data.
        """

        # Pop nested relationships, we need to handle them separately
        friends_data = validated_data.pop('friends', None)

        instance = super(ProfileSerializer, self).create(validated_data)

        # Add default avatar
        instance.avatar = "foreign_avatar.jpg"

    def update(self, instance, validated_data):
        """
        Updates and returns an instance of the `User` Model with validated data
        """

        # Pop nested relationships, we need to handle them separately
        friends_data = validated_data.pop('friends', None)

        # Call Super to update the Comment instance
        instance = super(ProfileSerializer, self).update(instance, validated_data)

        return instance

    class Meta:
        model = Author
        fields = ['id', 'host', 'displayname', 'friends', 'github_username', 'bio']


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
        model = Author
        include = ["uuid", "github_id", "avatar", "about"]
        read_only_fields = ['uuid']
