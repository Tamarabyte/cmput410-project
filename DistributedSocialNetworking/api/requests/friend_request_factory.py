from requests.auth import HTTPBasicAuth
from api.serializers import AuthorSerializer
import requests
import json


class FriendRequestFactory():
    """
    An Encapsulation for building FriendRequests
    """
    def post(self):
        raise NotImplementedError('`post()` must be implemented.')

    # Static Factory
    def create(node):
        if node.team_number == 5:
            return SocshizzleFriendRequest(node)
        if node.team_number == 8:
            return Team8FriendRequest(node)
        if node.team_number == 9:
            return HindlebookFriendRequest(node)
        else:
            raise NotImplementedError('node `%s` does not have a corresponding factory.' % node.host_name)

    create = staticmethod(create)


class HindlebookFriendRequest(FriendRequestFactory):
    """
    Hindlebook specific FriendRequest
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/friendrequest" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def post(self, author, friend):
        data = {"query": "friendrequest",
                "author": AuthorSerializer(author).data,
                "friend": AuthorSerializer(friend).data}
        return requests.post(url=self.url, headers={"content-type": "application/json"}, data=json.dumps(data), auth=self.auth)


class Team8FriendRequest(FriendRequestFactory):
    """
    Team 8 specific FriendRequest
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/friendrequest" % node.host

    def post(self, author, friend, requester_uuid="YourAuthSucks"):
        self.auth = (requester_uuid+":"+self.node.our_username,self.node.our_password)
        data = {"query": "friendrequest",
                "author": AuthorSerializer(author).data,
                "friend": AuthorSerializer(friend).data}
        return requests.post(url=self.url, headers={"content-type": "application/json"}, data=json.dumps(data), auth=self.auth)


class SocshizzleFriendRequest(FriendRequestFactory):
    """
    Socshizzle specific FriendRequest
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/friendrequest" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def post(self, author, friend):
        data = {"query": "friendrequest",
                "author": AuthorSerializer(author).data,
                "friend": AuthorSerializer(friend).data}
        return requests.post(url=self.url, headers={"content-type": "application/json"}, data=json.dumps(data), auth=self.auth)
