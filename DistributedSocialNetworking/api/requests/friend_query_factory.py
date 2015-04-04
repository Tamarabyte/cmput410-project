from requests.auth import HTTPBasicAuth
from api.serializers import AuthorSerializer
import requests


class FriendQueryRequestFactory():
    """
    An Encapsulation for building Author to Author friend querying
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    def post(self):
        raise NotImplementedError('`post()` must be implemented.')

    # Static Factory
    def create(node):
        if node.team_number == 5:
            return SocshizzleFriendQueryRequest(node)
        if node.team_number == 8:
            return Team8FriendQueryRequest(node)
        if node.team_number == 9:
            return HindlebookFriendQueryRequest(node)
        else:
            raise NotImplementedError('node `%s` does not have a corresponding factory.' % node.host_name)

    create = staticmethod(create)


class HindlebookFriendQueryRequest(FriendQueryRequestFactory):
    """
    Hindlebook specific FriendQuery
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/friends" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, uuid1, uuid2):
        self.url = self.url + "/%s/%s" % (uuid1, uuid2)
        return requests.get(url=self.url, auth=self.auth)

    def post(self, uuid, uuids=[]):
        self.url = self.url + "/%s" % uuid
        data = {"query": "friends",
                "author": uuid,
                "authors": uuids}
        return requests.get(url=self.url, data=data, auth=self.auth)


class Team8FriendQueryRequest(FriendQueryRequestFactory):
    """
    Team 8 specific FriendQuery
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/friends" % node.host

    def get(self, uuid1, uuid2, requester_uuid="YourAuthSucks"):
        self.auth = HTTPBasicAuth("%s:%s" % (requester_uuid, self.node.our_username) , self.node.our_password)
        self.url = self.url + "/%s/%s" % (uuid1, uuid2)
        return requests.get(url=self.url, auth=self.auth)

    def post(self, uuid, uuids=[], requester_uuid="YourAuthSucks"):
        self.auth = (requester_uuid+":"+self.node.our_username,self.node.our_password)
        self.url = self.url + "/%s" % uuid
        data = {"query": friends,
                "author": uuid,
                "authors": uuids}
        return requests.get(url=self.url, data=data, auth=self.auth)


class SocshizzleFriendQueryRequest(FriendQueryRequestFactory):
    """
    Socshizzle specific FriendQuery
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/friends" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, uuid1, uuid2):
        self.url = self.url + "/%s/%s" % (uuid1, uuid2)
        return requests.get(url=self.url, auth=self.auth)

    def post(self, uuid, uuids=[]):
        self.url = self.url + "/%s" % uuid
        data = {"query": "friends",
                "author": uuid,
                "authors": uuids}
        return requests.get(url=self.url, data=data, auth=self.auth)
