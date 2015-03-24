from urllib.request import urlopen
from urllib.error import HTTPError
import json
from Hindlebook.models import Node

# Module to hold outgoing API calls to get various info from other services.

def getForeignAuthor(uuid):
    # Function to get a foreign author with the given uuid.
    # Returns None if the object isn't found, otherwise returns a JSON String
    # of the given author. IMHO it should return None or the python object,
    # and we should do our stuff in DJANGO NOT AJAX but whatever. See the foreign
    # profile loading for an example of doing it in python...
    AuthorJSON = None
    for node in Node.objects.all():
        #Right now i'm just using our url schema for API...
        # like sigh I don't know how we'll do this since its
        # obviously not going to be generic.
        # guess it'll be a buncha if elses.
        if node.host == "localhost":
            continue
        try:
            url = node.host + "/api/author/" +uuid
            print(url)
            response = urlopen(url)
            str_response = response.readall().decode('utf-8')
            obj = json.loads(str_response)
            if obj != None:
                # for some reason model has author.uuid but
                # outputted json is author.id so yeah...
                # same with username/displayname
                obj['uuid'] = obj['id']
                obj['username'] = obj['displayname']
                #This should probably get grabbed from like a global var,
                # not be hardcoded but whatever.
                obj['avatar'] = 'default_avatar.jpg'
                obj['host'] = node.host
                AuthorJSON = json.dumps(obj)
                break
        except HTTPError as e:
            # Catch any pesky errors from other sites being down
            pass 
    return AuthorJSON

def getForeignAuthorPosts(uuid):
    # Function to get a foreign authors posts visible to the currently logged in user
    # Returns None if the foreign author's posts can't be found, otherwise returns the JSON
    # of the given posts.
    postsJSON = None
    for node in Node.objects.all():
        if node.host == "localhost":
            continue
        try:
            # Needs authentication.
            url = node.host + "/api/author/"+uuid+"/posts"
            print(url)
            response = urlopen(url)
            postsJSON = response.readall().decode('utf-8')
        except HTTPError as e:
            pass
    return postsJSON
