import json
import requests
import datetime
import dateutil.parser
from Hindlebook.models import Node, Author, Settings, Post
from api.serializers import NonSavingPostSerializer
from api.requests import AuthoredPostsRequestFactory, VisiblePostsRequestFactory, ProfileRequestFactory


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
# FriendRequestFactory(node).create().post(author, friend)  # Pass in the author objects, not the UUID
# VisiblePostsRequestFactory(node).create().get(uuid)   # All posts visible to UUID
# PublicPostsRequestFactory(node).create().get()        # All public posts
# AuthoredPostsRequestFactory(node).create().get(requester_uuid, author_uuid)   # Author's posts visible to Requester
# FriendQueryRequestFactory(node).create().get(author1_uuid, author2_uuid)     # get verison, friends/uuid/uuid
# FriendQueryRequestFactory(node).create().post(uuid, uuids)                  # bulk version, uuids must be a list
# PostRequestFactory(node).create().get(post_id)                       # Get Post
# PostRequestFactory(node).create().post(post_id, Post)                # Post Post
# PostRequestFactory(node).create().put(post_id, Post)                # Put Post


# Module to hold outgoing API calls to get various info from other services.

def getForeignAuthorPosts(requesterUuid, targetUuid, node):
    ''' Gets all posts created by targetUuid a user on host node that
        are visible by logged in user requestUuid and returns them '''

    request = AuthoredPostsRequestFactory.create(node)
    response = request.get(requesterUuid, targetUuid)

    if(response.status_code != 200):
        # Node not reachable
        print("Node %s returned us status code %s!!!" % (node.host_name, response.status_code))
        return []

    # Get the JSON returned
    postsJSON = response.json()

    # Turn the JSON into Post objects!
    serializer = NonSavingPostSerializer(data=postsJSON["posts"], many=True)
    if serializer.is_valid(raise_exception=True):
        posts = serializer.save()
    return posts


def getForeignStreamPosts(author, min_time):
    ''' Gets all the posts foreign posts that should be displayed in user denoted
        by uuid's stream. Should be called to create the stream for user uuid
        returns a list of post objects.'''
    posts = []
    postsJSON = None
    for node in Node.objects.all():

        # Skip our node, don't want to ask ourselves unecessarily.
        if node == Settings.objects.all().first().node:
            continue

        # Make a request for this nodes visible posts
        request = VisiblePostsRequestFactory.create(node)
        response = request.get(author.uuid)

        if(response.status_code != 200):
            # Node not reachable
            print("Node %s returned us status code %s!!!" % (node.host_name, response.status_code))
            continue

        # Get the JSON returned
        postsJSON = response.json()

        # Turn the JSON into Post objects!
        # If the serializer throws exceptions during validation, it will throw a HTTP 400
        # Don't catch it!
        serializer = NonSavingPostSerializer(data=postsJSON["posts"], many=True)
        if serializer.is_valid(raise_exception=True):
            newposts = serializer.save()

        # We only want newish posts ?
        if min_time is not None:
            posts += filter(lambda p: p.pubDate > min_time, newposts)
        else:
            posts += newposts
    return posts


def getForeignAuthor(uuid):
    author = None
    for node in Node.objects.all():
        if node == Settings.objects.all().first().node:
            continue
        obj = ProfileRequestFactory.create(node).get(uuid).json()
        try:
            author = Author.objects.get(uuid=uuid, node = node)
            # since there is no defined profile JSON, can't expect these to be in the request.
            # best to use obj.get('github_id', None) which will give you None if not in the request
            # indexing will throw an error
            author.github_id = obj['github_id']
            author.about = obj['about']
            author.username = obj['displayname']
            author.save()
            break
        except Author.DoesNotExist:
            author = Author.objects.create(uuid=uuid, username=obj['displayname'],
                                           node=node, about=obj["about"], github_id=obj['github_id'])
            author.save()
            break
    return author
