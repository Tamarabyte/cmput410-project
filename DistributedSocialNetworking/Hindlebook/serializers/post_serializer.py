from django.forms import widgets
from django.db import IntegrityError, transaction
from rest_framework import serializers
from Hindlebook.models import Post


class PostSerializer(serializers.Serializer):
    content = serializers.CharField()
    pubDate = serializers.DateTimeField()
    guid = serializers.CharField(max_length=40)
    title = serializers.CharField(max_length=40)
    description = serializers.CharField(max_length=40)
    content_type = serializers.CharField(max_length=40)
    source = serializers.CharField(max_length=100)
    origin = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Post` instance, given the validated data.
        """
        with transaction.atomic(): # TODO: remove this?
            post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        """
        Update and return an existing `Post` instance, given the validated data.
        """
        with transaction.atomic(): # TODO: remove this?
            instance.content = validated_data.get('text', instance.text)
            instance.pubDate = validated_data.get('pub_date', instance.pub_date)
            instance.guid = validated_data.get('guid', instance.guid)
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.content_type = validated_data.get('content_type', instance.content_type)
            instance.source = validated_data.get('source', instance.source)
            instance.origin = validated_data.get('origin', instance.origin)
            instance.save()
        return instance
