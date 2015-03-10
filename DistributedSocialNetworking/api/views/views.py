from django.shortcuts import render, render_to_response
from django.template import Template
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from Hindlebook.models import User, Post
from Hindlebook.serializers import PostSerializer
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status


class PostDetail(APIView):
    """ GET, POST, or PUT an author post """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get_object(self, uuid):
        try:
            return Post.objects.get(uuid=uuid)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, postID, format=None):
        post = self.get_object(postID)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def post(self, request, postID, format=None):
        post = self.get_object(postID)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, postID, format=None):
        post = self.get_object(postID)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            author = User.objects.get(uuid=authorID)
            friend = User.objects.get(uuid=friendID)

            if (friend not in author.getFriendRequests()):
                author.follows.add(friend)
        except:
            return HttpResponse(status=404)

        return HttpResponse(status=200)


class AuthorPosts(APIView):
    """ GET posts from given author """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, authorID, format=None):
        try:
            postAuthor = User.objects.get(uuid=authorID)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        posts = postAuthor.getAuthoredPosts()

        returnPosts = []
        for post in posts:
            serializer = PostSerializer(post)
            returnPosts.append(serializer.data)

        return Response(json.dumps({"posts":returnPosts}))


class PublicPosts(APIView):
    """ GET all public posts """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, requst, format=None):
        # Filter to get public posts, 0 is currently public (Should make it a text field)
        posts = Post.objects.filter(privacy=0)

        returnPosts = []
        for post in posts:
            serializer = PostSerializer(post)
            returnPosts.append(serializer.data)

        return Response(json.dumps({"posts":returnPosts}))
