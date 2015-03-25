import json


from Hindlebook.models import Node, Author, Settings, Post
from api.requests.authored_posts_factory import AuthoredPostsRequestFactory
from api.requests.visible_posts_factory import VisiblePostsRequestFactory
from api.serializers import NonSavingPostSerializer
import datetime
import dateutil.parser
# Key for the Request Factories
#
# Appending .json() to the end of these gets the json
# or you can store it and get the status_code
#
# eg/ request = FriendRequestFactory(node.host).create()
#     response = request.post(author, friend)
#     if response.status_code != 200:
#          explode()
#     data = response.json()
#
# FriendRequestFactory(node.host).create().post(author, friend)  # Pass in the author objects, not the UUID
# VisiblePostsRequestFactory(node.host).create().get(uuid)   # All posts visible to UUID
# PublicPostsRequestFactory(node.host).create().get()        # All public posts
# AuthoredPostsRequestFactory(node.host).create().get(requester_uuid, author_uuid)   # Author's posts visible to Requester
# FriendQueryRequestFactory(node.host).create().get(author1_uuid, author2_uuid)     # get verison, friends/uuid/uuid
# FriendQueryRequestFactory(node.host).create().post(uuid, uuids)                  # bulk version, uuids must be a list
# PostRequestFactory(node.host).create().get(post_id)                       # Get Post
# PostRequestFactory(node.host).create().post(post_id, Post)                # Post Post
# PostRequestFactory(node.host).create().put(post_id, Post)                # Put Post


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


def getForeignAuthorPosts(uuid, host):
    raise Exception("getForeignAuthorPosts not implemented")
    postsJSON = AuthoredPostsRequestFactory.create(host).get(self.request.user.author, uuid).json()
    
    return postsJSON

def getForeignStreamPosts(uuid,min_time):
    ''' Gets all the posts foreign posts that should be displayed in user denoted
        by uuid's stream. Should be called to create the stream for user uuid 
        returns a list of post objects.'''
    posts = []
    for node in Node.objects.all():
        # Skip our node, don't want to ask ourselves unecessarily.
        if node == Settings.objects.all().first().node:
            continue
        postsJSON = VisiblePostsRequestFactory.create(node.host,uuid).get(uuid).json()
        try:
            serializer = NonSavingPostSerializer(data=postsJSON["posts"],many=True)
            if serializer.is_valid(raise_exception=True):
                newposts = serializer.save()
        except Exception as e:
            print("exception raised!")
            print(str(e))
        for post in newposts:
            try:
                if min_time != None:
                    if post.pubDate > min_time:
                        posts.append(post)
                else:
                    posts.append(post)
            except Exception as e:
                print(str(e))
                
    return posts



def getForeignAuthor(uuid,host="http://dev.tamarabyte.com"):
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

