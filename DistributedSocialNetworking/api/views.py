from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from Hindlebook.models import User
import json


def friend2friendQuery(request, authorID1, authorID2):
    """ Handles friend2friend querying via GET """
    if (request.method != "GET"):
        # Raises a 405, Method not allowed
        return HttpResponse(status=405)

    # Get the author objects from their given IDs, 404 if they don't exist
    try:
        author1 = User.objects.get(id=authorID1)
        author2 = User.objects.get(id=authorID2)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    # Check if the authors are 'real' friends
    if (author2 in author1.getFriends() and author1 in author2.getFriends()):
        friends = "YES"
    else:
        friends = "NO"

    # Return a JSON object based from https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
    # Hindle's format specifies "friends":[id1, id2], and also "friends":"YES"
    # Does this make more sense: "authors":[id1, id2], and "friends":"YES"??
    return JsonResponse({"query": "friends", "authors": [authorID1, authorID2], "friends": friends})


def friendQuery(request, authorID1):
    """ Handles friend querying via POST with JSON """
    if (request.method != "POST"):
        # Raises a 405, Method Not Allowed
        return HttpResponse(status=405)

    # Load the POSTed data as JSON
    JSONrequest = json.loads(request.body.decode('utf-8'))

    # Check if valid POST data, return Bad Request
    if ('author' not in JSONrequest):
        return HttpResponse(status=400)
    elif ('authors' not in JSONrequest):
        return HttpResponse(status=400)
    elif (str(authorID1) != str(JSONrequest['author'])):
        return HttpResponse(status=400)

    # Get the author object from the given ID, return 404 if it doesn't exist
    try:
        author1 = User.objects.get(id=authorID1)
    except Author.DoesNotExist:
        return HttpResponse(status=404)

    friends = []

    # Loop through all POSTed authors, check if friends with author1
    for authorID2 in JSONrequest['authors']:
        try:
            author2 = User.objects.get(id=authorID2)
            if (author2 in author1.getFriends() and
               author1 in author2.getFriends()):
                friends.append(authorID2)
        except:
            # Silently ignore author IDs which don't exist
            pass

    # Return a JSON object based from https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
    return JsonResponse({"query": "friends", "author": authorID1, "friends": friends})


def friendRequest(request):
    """ Handles friend request via POST with JSON """
    if (request.method != "POST"):
        # Raises a 405, Method not allowed
        return HttpResponse(status=405)

    # Load the POSTed data as JSON
    JSONrequest = json.loads(request.body.decode('utf-8'))

    # If
    if ('author' not in JSONrequest or 'id' not in JSONrequest['author']):
        return HttpResponse(status=400)
    elif ('friend' not in JSONrequest or 'id' not in JSONrequest['friend']):
        return HttpResponse(status=400)

    authorID = JSONrequest['author']['id']
    friendID = JSONrequest['friend']['id']

    try:
        author = User.objects.get(id=authorID)
        friend = User.objects.get(id=friendID)

        # Don't send repeated friend requests
        if (friend not in author.getFriendRequests()):
            author.follows.add(friend)
    except:
        return HttpResponse(status=404)

    return HttpResponse(status=200)
