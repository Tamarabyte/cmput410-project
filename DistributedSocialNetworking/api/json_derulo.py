import json
import requests
import datetime
import dateutil.parser

from Hindlebook.models import Node, Author, Settings, Post
from api.requests import AuthoredPostsRequestFactory, VisiblePostsRequestFactory, ProfileRequestFactory
from api.serializers import NonSavingPostSerializer


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


def author_update_or_create(targetUUID,node):
    ''' Takes in a uuid and a node and update or creates that author in our
        DB after requesting the info from that node '''
    author = None

    obj = ProfileRequestFactory.create(node.host).get(targetUUID).json()
    try:
        author = Author.objects.get(uuid=targetUUID,node = node)
        author.github_id = obj['github_id']
        author.about = obj['about']
        author.username = obj['displayname']
        author.save()
    except Author.DoesNotExist:
        author= Author.objects.create(uuid=targetUUID,username=obj['displayname'],
                                        node=node,about=obj["about"],github_id=obj['github_id'])
        author.save()
    return author


def getForeignAuthorPosts(requesterUuid,targetUuid, node):
    ''' Gets all posts created by targetUuid a user on host node that
        are visible by logged in user requestUuid and returns them '''
    postsJSON = AuthoredPostsRequestFactory.create(node.host).get(requesterUuid,
                                                                    targetUuid).json()
    serializer = NonSavingPostSerializer(data=postsJSON["posts"],many=True)
    posts = None
    if serializer.is_valid(raise_exception=True):
        posts = serializer.save()
    return posts

def getForeignStreamPosts(userUuid,min_time):
    ''' Gets all the posts foreign posts that should be displayed in user denoted
        by uuid's stream. Should be called to create the stream for user uuid 
        returns a list of post objects.'''
    posts = []
    for node in Node.objects.all():
        # Skip our node, don't want to ask ourselves unecessarily.
        if node == Settings.objects.all().first().node:
            continue
        try:
            postsJSON = VisiblePostsRequestFactory.create(node.host,userUuid).get(userUuid).json()
        except Exception as e:
            print(node)
            print(str(e))
        try:
            serializer = NonSavingPostSerializer(data=postsJSON["posts"],many=True)
            if serializer.is_valid(raise_exception=True):
                newposts = serializer.save()
        except Exception as e:
            print("exception raised!")
            print(str(e))
        if min_time != None:
            posts += filter(lambda p: p.pubDate > min_time,newposts)
        else:
            posts += newposts
    return posts



def getForeignAuthor(uuid):
    author = None
    for node in Node.objects.all():
        if node == Settings.objects.all().first().node:
            continue
        obj = ProfileRequestFactory.create(node.host).get(uuid).json()
        try:
            author = Author.objects.get(uuid=uuid,node = node)
            author.github_id = obj['github_id']
            author.about = obj['about']
            author.username = obj['displayname']
            author.save()
            break
        except Author.DoesNotExist:
            author= Author.objects.create(uuid=uuid,username=obj['displayname'],
                                            node=node,about=obj["about"],github_id=obj['github_id'])
            author.save()
            break
    return author

