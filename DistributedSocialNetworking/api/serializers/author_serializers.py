from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Author, Node


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
    host = serializers.CharField(source='node')
    id = serializers.CharField(source='uuid')
    friends = AuthorSerializer(many=True)
    # github_username = serializers.CharField(source='github_id', allow_null=True, default=Author._meta.get_field('github_id').get_default())
    # bio = serializers.CharField(source='about', allow_null=True, default=Author._meta.get_field('about').get_default())

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """

        ret = super(ProfileSerializer, self).to_representation(instance)

        # Node to host string
        node = ret.pop('host')
        ret['host'] =  Node.objects.filter(host=node).first().host

        return ret

    def validate_host(self, value):
        node = Node.objects.filter(host=value).first()
        if node is None:
            print("Unknown host '%s' during serialization, throwing exception" % value)
            logger.log("Unknown host '%s' during serialization, throwing exception" % value)
            raise serializers.ValidationError('Invalid or Unknown Host: %s' % value)
        return node

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

        # We don't update hosts
        node = validated_data.pop('node', None)

        # Call Super to update the Comment instance
        instance = super(ProfileSerializer, self).update(instance, validated_data)

        return instance

    class Meta:
        model = Author
        fields = ['id', 'host', 'displayname', 'friends']


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
