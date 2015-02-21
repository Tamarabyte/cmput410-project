from django.shortcuts import render
from django.http import HttpResponse, Http404
from Hindlebook.models import Author
import json

# Just a temporary blank homepage for now..
def home(request):
    html = "<html><body>Server is Working! - Hindlebook!</body></html>"

    # Should use render() with a template in the future
    return HttpResponse(html)


def friend2friendQuery(request, authorID1, authorID2):
    if (request.method == "POST"):
        # We should only be handling GET requests for friend2friend? So give a 404 if POST?        
        raise Http404    
    
    # Try getting the given author objects from their IDs, return 404 if they don't exist
    try:
        author1 = Author.objects.get(id = authorID1)
        author2 = Author.objects.get(id = authorID2)
    except Author.DoesNotExist:
        raise Http404

    # Check if the authors are 'real' friends
    if (author2 in author1.getFriends() and author1 in author2.getFriends()):
        friends = "YES"
    else:
        friends = "NO"

    # Return a JSON object based from https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
    # Note that hindle's format specifies "friends":[id1, id2], and also "friends":"YES"
    JSONresponse = json.dumps({"query":"friends", "authors":[authorID1, authorID2], "friends":friends})
    return HttpResponse(JSONresponse)
