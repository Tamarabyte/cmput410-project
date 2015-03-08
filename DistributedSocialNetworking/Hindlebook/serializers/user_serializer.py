from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import User


class UserSerializer(serializers.Serializer):
    uuid = serializers.CharField(max_length=40)
    github_id = serializers.CharField(max_length=30)
    about = serializers.CharField(max_length=250)
    host = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.github_id = validated_data.get('github_id', instance.github_id)
        instance.about = validated_data.get('about', instance.about)
        instance.host = validated_data.get('host', instance.host)
        instance.save()
        return instance
