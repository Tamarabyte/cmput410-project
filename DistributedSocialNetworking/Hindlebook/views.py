from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from Hindlebook.models import Author
import json

# Just a temporary blank homepage for now..
def home(request):
    html = "<html><body>Server is Working! - Hindlebook!</body></html>"

    # Should use render() with a template in the future
    return HttpResponse(html)

# Handles friend2friend querying via GET
def friend2friendQuery(request, authorID1, authorID2):
    if (request.method == "POST"):
        # We should only be handling GET requests for friend2friend? So give a 404 if POST?        
        raise Http404("Should be a GET request")
    
    # Try getting the author objects from their given IDs, return 404 if they don't exist
    try:
        author1 = Author.objects.get(id = authorID1)
        author2 = Author.objects.get(id = authorID2)
    except Author.DoesNotExist:
        raise Http404("An author doesn't exist")

    # Check if the authors are 'real' friends
    if (author2 in author1.getFriends() and author1 in author2.getFriends()):
        friends = "YES"
    else:
        friends = "NO"

    # Return a JSON object based from https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
    # Note that hindle's format specifies "friends":[id1, id2], and also "friends":"YES"
    return JsonResponse({"query":"friends", "authors":[authorID1, authorID2], "friends":friends})

# Handles friend querying via POST with JSON
def friendQuery(request, authorID1):
    if (request.method == "GET"):
        # We should only be handling POST requests for friend query? So give a 404 if GET?        
        raise Http404("Should be a POST request")

    # Load the POSTed data as JSON
    JSONrequest = json.loads(request.body)

    # Check if valid POST data
    if (not 'author' in JSONrequest):
        raise Http404("Missing author ID")
    elif (not 'authors' in JSONrequest):
        raise Http404("Missing author list")
    elif (str(authorID1) != str(JSONrequest['author'])):
        raise Http404("Inconsistent author ID")

    # Try getting the author object from the given ID, return 404 if it doesn't exist
    try:
        author1 = Author.objects.get(id = authorID1)
    except Author.DoesNotExist:
        raise Http404("Author doesn't exist")

    friends = []

    # Loop through all POSTed authors, check if friends with author1
    for authorID2 in JSONrequest['authors']: 
        try:
            author2 = Author.objects.get(id = authorID2)         
            if (author2 in author1.getFriends() and author1 in author2.getFriends()):
                friends.append(authorID2)
        except:
            # Should it throw a 404 if the POST author list contains an invalid ID??
            pass

    # Return a JSON object based from https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
    return JsonResponse({"query":"friends", "author":authorID1, "friends":friends})
