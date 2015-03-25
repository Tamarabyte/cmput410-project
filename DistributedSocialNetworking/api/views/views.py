from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Template
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from Hindlebook.models import Author, Post
from api.serializers import PostSerializer, FriendQuerySerializer
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from api.json_derulo import getForeignAuthor


class Friend2Friend(APIView):
    """ GET a friend2friend query """

    def get(self, request, authorID1, authorID2, format=None):
        try:
            author1 = Author.objects.get(uuid=authorID1)
            author2 = Author.objects.get(uuid=authorID2)
        except Author.DoesNotExist:
            return HttpResponse(status=404)

        if (author2 in author1.getFriends() and author1 in author2.getFriends()):
            friends = "YES"
        else:
            friends = "NO"

        return JsonResponse({"query": "friends", "authors": [authorID1, authorID2], "friends": friends})


class FriendRequest(APIView):
    """ POST a friend request """

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

        author = None
        friend = None
        local = True

        try:
            author = Author.objects.get(uuid=authorID)
            if Author.objects.get(uuid=authorID).node.host != "localhost":
                local = False
        except Author.DoesNotExist:
            author = getForeignAuthor(authorID)
            local = False
        except:
            print("yeah okay")
        if not local:
            author = getForeignAuthor(authorID)
        try:
            # Can just call get_object_or_404 as in order to
            # friend request someone they have to have viewed their
            # profile, meaning json_derulo added them already.
            friend = get_object_or_404(Author, uuid=friendID)
            if author and friend:
                if friend.node.host != "localhost" and author.node.host !="localhost":
                    # Don't handle friend requests between two foreign users
                    return HttpResponse(status=404)
                if (friend not in author.friends.all()):
                    author.friends.add(friend)

                if (friend not in author.follows.all()):
                    author.follows.add(friend)
            else:
                print("404 because couldn't find friend+author")
                return HttpResponse(status=404)
        except:
            return HttpResponse(status=404)

        return HttpResponse(status=200)


class UnfriendRequest(APIView):
    """ POST an unfriend query """

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
            author = get_object_or_404(Author, uuid=authorID)
            friend = get_object_or_404(Author, uuid=friendID)
            # If someone requsets an unfriend this is either a
            # cancellation of a friend request, or termination
            # of a friend relationship, so we have to remove from
            # the author from the friends list of friends if it exists
            # to terminate an existing friend relationship, not leave
            # a hanging friend request from the friend immediately
            # after termination of their relationship.
            if (friend in author.friends.all()):
                author.friends.remove(friend)
            if (author in friend.friends.all()):
                friend.friends.remove(author)
        except:
            return HttpResponse(status=404)

        return HttpResponse(status=200)


class FollowRequest(APIView):
    """ POST a follow query """

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
            author = get_object_or_404(Author, uuid=authorID)
            friend = get_object_or_404(Author, uuid=friendID)

            if (friend not in author.follows.all()):
                author.follows.add(friend)
        except:
            return HttpResponse(status=404)

        return HttpResponse(status=200)


class UnfollowRequest(APIView):
    """ POST a unfollow query """

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
            author = get_object_or_404(Author, uuid=authorID)
            friend = get_object_or_404(Author, uuid=friendID)
            if (friend in author.follows.all()):
                author.follows.remove(friend)
        except:
            return HttpResponse(status=404)

        return HttpResponse(status=200)
