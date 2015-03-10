from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Post, User, Comment
from api.serializers.author_serializers import AuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), read_only=False)

    author = AuthorSerializer(read_only=False)

    class Meta:
            model = Comment

            fields = ('author', 'comment', 'pubDate', 'guid')
