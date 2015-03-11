from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Template
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from Hindlebook.models import User, Post
# from Hindlebook.serializers import PostSerializer
from api.serializers.post_serializer import PostSerializer
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class Friend2Friend(APIView):
    """ GET a friend2friend query """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, authorID1, authorID2, format=None):
        try:
            author1 = User.objects.get(uuid=authorID1)
            author2 = User.objects.get(uuid=authorID2)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        if (author2 in author1.getFriends() and author1 in author2.getFriends()):
            friends = "YES"
        else:
            friends = "NO"

        return JsonResponse({"query": "friends", "authors": [authorID1, authorID2], "friends": friends})


class FriendQuery(APIView):
    """ POST a friend query """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request, authorID1, format=None):
        JSONrequest = json.loads(request.body.decode('utf-8'))

        if ('author' not in JSONrequest):
            return HttpResponse(status=400)
        elif ('authors' not in JSONrequest):
            return HttpResponse(status=400)
        elif (type(JSONrequest['authors']) is not list):
            return HttpResponse(status=400)
        elif (str(authorID1) != str(JSONrequest['author'])):
            return HttpResponse(status=400)

        try:
            author1 = User.objects.get(uuid=authorID1)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        friends = []

        for authorID2 in JSONrequest['authors']:
            try:
                author2 = User.objects.get(uuid=authorID2)
                if (author2 in author1.getFriends() and author1 in author2.getFriends()):
                    friends.append(authorID2)
            except:
                pass

        return JsonResponse({"query": "friends", "author": authorID1, "friends": friends})


class FriendRequest(APIView):
    """ POST a friend query """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        JSONrequest = json.loads(request.body.decode('utf-8'))
        if ('author' not in JSONrequest):
            return HttpResponse(status=400)
        elif (type(JSONrequest['author']) is not dict):
            return HttpResponse(status=400)
        elif ('id' not in JSONrequest['author']):
            return HttpResponse(status=400)
        elif ('friend' not in JSONrequest or 'id' not in JSONrequest['friend']):
            return HttpResponse(status=400)
        elif (type(JSONrequest['friend']) is not dict):
            return HttpResponse(status=400)
        elif ('id' not in JSONrequest['friend']):
            return HttpResponse(status=400)

        authorID = JSONrequest['author']['id']
        friendID = JSONrequest['friend']['id']

        try:
            author = get_object_or_404(User, uuid=authorID)
            friend = get_object_or_404(User, uuid=friendID)

            if (friend not in author.follows.all()):
                author.follows.add(friend)
        except:
            return HttpResponse(status=404)

        return HttpResponse(status=200)

class UnfriendRequest(APIView):
    """ POST a friend query """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        JSONrequest = json.loads(request.body.decode('utf-8'))
        if ('author' not in JSONrequest):
            return HttpResponse(status=400)
        elif (type(JSONrequest['author']) is not dict):
            return HttpResponse(status=400)
        elif ('id' not in JSONrequest['author']):
            return HttpResponse(status=400)
        elif ('friend' not in JSONrequest or 'id' not in JSONrequest['friend']):
            return HttpResponse(status=400)
        elif (type(JSONrequest['friend']) is not dict):
            return HttpResponse(status=400)
        elif ('id' not in JSONrequest['friend']):
            return HttpResponse(status=400)

        authorID = JSONrequest['author']['id']
        friendID = JSONrequest['friend']['id']

        try:
            author = get_object_or_404(User, uuid=authorID)
            friend = get_object_or_404(User, uuid=friendID)

            if (friend in author.follows.all()):
                author.follows.remove(friend)
        except:
            return HttpResponse(status=404)

        return HttpResponse(status=200)
