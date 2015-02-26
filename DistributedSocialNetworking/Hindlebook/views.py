from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from Hindlebook.models import Author
import json


def home(request):
    """ Handles the home URL """
    html = "<html><body>Server is Working! - Hindlebook!</body></html>"

    # Should use render() with a template in the future
    return HttpResponse(html)


def friend2friendQuery(request, authorID1, authorID2):
    """ Handles friend2friend querying via GET """
    if (request.method != "GET"):
        # Should raise a better error
        raise Http404("Should be a GET request")

    # Get the author objects from their given IDs, 404 if they don't exist
    try:
        author1 = Author.objects.get(id=authorID1)
        author2 = Author.objects.get(id=authorID2)
    except Author.DoesNotExist:
        raise Http404("An author doesn't exist")

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
        # Should raise a better error
        raise Http404("Should be a POST request")

    # Load the POSTed data as JSON
    JSONrequest = json.loads(request.body.decode('utf-8'))

    # Check if valid POST data
    if ('author' not in JSONrequest):
        raise Http404("Missing author ID")
    elif ('authors' not in JSONrequest):
        raise Http404("Missing author list")
    elif (str(authorID1) != str(JSONrequest['author'])):
        raise Http404("Inconsistent author ID")

    # Get the author object from the given ID, return 404 if it doesn't exist
    try:
        author1 = Author.objects.get(id=authorID1)
    except Author.DoesNotExist:
        raise Http404("Author doesn't exist")

    friends = []

    # Loop through all POSTed authors, check if friends with author1
    for authorID2 in JSONrequest['authors']:
        try:
            author2 = Author.objects.get(id=authorID2)
            if (author2 in author1.getFriends() and
               author1 in author2.getFriends()):
                friends.append(authorID2)
        except:
            # Maybe throw 404 if the POST author list contains an invalid ID??
            pass

    # Return a JSON object based from https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
    return JsonResponse({"query": "friends", "author": authorID1, "friends": friends})
