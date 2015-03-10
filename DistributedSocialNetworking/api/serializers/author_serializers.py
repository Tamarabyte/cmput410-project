from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import User


class UserSerializer(serializers.ModelSerializer):
    displayname = serializers.CharField('User.username')
    host = serializers.CharField('User.username')
    id = serializers.CharField('User.username')

    class Meta:
        model = User;
        fields = ["displayname, host, id"]
