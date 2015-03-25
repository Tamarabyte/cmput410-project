from urllib.request import urlopen
from urllib.error import HTTPError
import json
from Hindlebook.models import Node, Author, Settings

# Key for the Request Factories
#
# Appending .json() to the end of these gets the json
# or you can store it and get the status_code
#
# eg/ request = FriendRequestFactory(node.host)
#     response = request.post(author, friend)
#     if response.status_code != 200:
#          explode()
#     data = response.json()
#
# FriendRequestFactory(node.host).post(author, friend)  # Pass in the author objects, not the UUID
# VisiblePostsRequestFactory(node.host).get(uuid)   # All posts visible to UUID
# PublicPostsRequestFactory(node.host).get()        # All public posts
# AuthoredPostsRequestFactory(node.host).get(requester_uuid, author_uuid) # Author's posts visible to Requester
# FriendQueryRequestFactory(node.host).get(author1_uuid, author2_uuid)
#



# Module to hold outgoing API calls to get various info from other services.


def author_update_or_create(uuid,host):
    author = None
    try:
        url = host + "/api/author/" +uuid
        print(url)
        response = urlopen(url)
        str_response = response.readall().decode('utf-8')
        obj = json.loads(str_response)
        node = None
        try:
            node = Node.objects.get(host = host)
        except:
            raise Exception("Failure finding node: %s" % host)
        if obj != None:
            # for some reason model has author.uuid but
            # outputted json is author.id so yeah...
            # same with username/displayname
            obj['uuid'] = obj['id']
            #This should probably get grabbed from like a global var,
            # not be hardcoded but whatever.
            obj['avatar'] = 'default_avatar.jpg'
            obj['host'] = node.host
            try:
                author = Author.objects.get(uuid=uuid,node = node)
                author.github_id = obj['github_id']
                author.about = obj['about']
                author.username = obj['displayname']
                author.avatar = obj['avatar']
                author.save()
            except Author.DoesNotExist:
                author= Author.objects.create(uuid=uuid,username=obj['displayname'],
                                                node=node,about=obj["about"],
                                                avatar=obj['avatar'],github_id=obj['github_id'])
                author.save()
    except HTTPError as e:
        # Catch any pesky errors from other sites being down
        print("Http error getting stuff: " + type(e))
        pass
    return author


# Deprecated function. No longer use, references to this function should be removed.
# and then the function itself. I have not yet done this as I don't want to fix all
# the places I use this code before pushing the other function for mark
# Deprecated because Mark is a big meanie.
def getForeignAuthor(uuid):
    # Function to get a foreign author with the given uuid.
    # Returns None if the author isn't found, otherwise creates/updates that
    # users info in our DB with the infor returned from the foreign hosts and
    # returns the author object.
    author = None
    for node in Node.objects.all():
        #Right now i'm just using our url schema for API...
        # like sigh I don't know how we'll do this since its
        # obviously not going to be generic.
        # guess it'll be a buncha if elses.
        if node == Settings.objects.all().first():
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
                #This should probably get grabbed from like a global var,
                # not be hardcoded but whatever.
                obj['avatar'] = 'default_avatar.jpg'
                obj['host'] = node.host
                try:
                    author = Author.objects.get(uuid=uuid)
                    author.github_id = obj['github_id']
                    author.about = obj['about']
                    author.node = node
                    author.username = obj['displayname']
                    author.avatar = obj['avatar']
                    author.save()
                except Author.DoesNotExist:
                    author= Author.objects.create(uuid=uuid,username=obj['displayname'],
                                                    node=node,about=obj["about"],
                                                    avatar=obj['avatar'],github_id=obj['github_id'])
                    author.save()
                break
        except HTTPError as e:
            # Catch any pesky errors from other sites being down
            print("Http error getting stuff: " + type(e))
            pass
    return author

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
