import json
import requests
import datetime
import dateutil.parser
from Hindlebook.models import Node, Author, Post, Comment
from api.serializers import PostSerializer
from api.requests import AuthoredPostsRequestFactory, VisiblePostsRequestFactory, ProfileRequestFactory, PostRequestFactory


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

def json_to_posts(json, node):
    if (node.team_number == 8):
        # Team 8 doesn't follow spec so json['posts'] will error out.
        # hooray!
        posts = json
    else:
        posts = json["posts"]

    out = []

    for p in posts:
        guid = p.get('guid', None)
        if guid is None:
            # Bad json
            continue

        post = Post.objects.filter(guid=guid).first()
        if post is None:
            # create post
            serializer = PostSerializer(data=p)
            serializer.is_valid(raise_exception=True)
            post = serializer.save(node=node)
        else:
            # update post
            serializer = PostSerializer(post, data=p)
            serializer.is_valid(raise_exception=True)
            post = serializer.save(node=node)
            out.append(post)

    return out



def getForeignAuthorPosts(requesterUuid, targetUuid, node):
    ''' Gets all posts created by targetUuid a user on host node that
        are visible by logged in user requestUuid and returns them '''

    request = AuthoredPostsRequestFactory.create(node)
    response = request.get(targetUuid, requesterUuid)

    if(response.status_code != 200):
        # Node not reachable
        print("Node %s returned us status code %s!!!" % (node.host_name, response.status_code))
        return []

    # Get the JSON returned
    postsJSON = response.json()
    # Turn the JSON into Post objects!
    posts = json_to_posts(postsJSON, node)

    return posts


def getForeignStreamPosts(author, min_time):
    ''' Gets all the posts foreign posts that should be displayed in user denoted
        by uuid's stream. Should be called to create the stream for user uuid
        returns a list of post objects.'''
    posts = []
    postsJSON = None
    for node in Node.objects.getActiveNodes():

        # Make a request for this nodes visible posts

        request = VisiblePostsRequestFactory.create(node)
        response = request.get(author.uuid)

        if(response.status_code != 200):
            # Node not reachable
            print("Node %s returned us status code %s!!!" % (node.host_name, response.status_code))
            continue

        # Get the JSON returned
        postsJSON = response.json()


        # Turn the JSON into Post objects in the DB!
        json_to_posts(postsJSON, node)

    return []


def getForeignAuthor(uuid):
    author = None
    for node in Node.objects.getActiveNodes():

        request = ProfileRequestFactory.create(node)
        response = request.get(uuid)
        if(response.status_code != 200):
            # Node not reachable
            print("Node %s returned us status code %s!!!" % (node.host_name, response.status_code))
            continue

        obj = response.json()

        try:
            author = Author.objects.get(uuid=uuid, node=node)
            # since there is no defined profile JSON, can't expect these to be in the request.
            # best to use obj.get('github_id', Default) which will give you Default if not in the request
            # indexing will throw an error
            author.github_id = obj.get('github_username', "")
            author.about = obj.get('bio', "")
            author.username = obj.get('displayname', "Unknown Author")
            author.avatar = "foreign_avatar.jpg"
            author.save()
            break
        except Author.DoesNotExist:
            author = Author.objects.create(uuid=uuid, username=obj.get('displayname', "Unknown Author"),
                                           node=node, about=obj.get('bio', ""), github_id=obj.get('github_username', ""),
                                           avatar="foreign_avatar.jpg")
            author.save()
            break
    return author
