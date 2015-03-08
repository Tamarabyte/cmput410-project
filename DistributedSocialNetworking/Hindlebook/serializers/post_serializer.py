from django.forms import widgets
from django.db import IntegrityError, transaction
from rest_framework import serializers
from Hindlebook.models import Post

class PostSerializer(serializers.Serializer):
    text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    uuid = serializers.CharField(max_length=40)
    title = serializers.CharField(max_length=40)
    description = serializers.CharField(max_length=40)
    content_type = serializers.CharField(max_length=40)
    source = serializers.CharField(max_length=100)
    origin = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Post` instance, given the validated data.
        """
        with transaction.atomic():
            post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        """
        Update and return an existing `Post` instance, given the validated data.
        """
        with transaction.atomic():
            instance.text = validated_data.get('text', instance.text)
            instance.pub_date = validated_data.get('pub_date', instance.pub_date)
            instance.uuid = validated_data.get('uuid', instance.uuid)
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.content_type = validated_data.get('content_type', instance.content_type)
            instance.source = validated_data.get('source', instance.source)
            instance.origin = validated_data.get('origin', instance.origin)
            instance.save()
        return instance
