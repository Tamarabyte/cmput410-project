# from api.requests import HINDLEBOOK, DEV_HINDLEBOOK, TEST
from requests.auth import HTTPBasicAuth
from api.serializers import AuthorSerializer
import requests

HINDLEBOOK = {
    'host': "hindlebook.tamarabyte.com",
    'username': "hindlebook.tamarabyte.com",
    'password': "test",
    'port': ''
}

DEV_HINDLEBOOK = {
    'host': "dev.hindlebook.tamarabyte.com",
    'username': "dev.hindlebook.tamarabyte.com",
    'password': "test",
    'port': ''
}


class FriendRequestFactory():
    """
    An Encapsulation for building FriendRequests
    """
    def post(self):
        raise NotImplementedError('`post()` must be implemented.')

    # Static Factory
    def create(host):
        if host == HINDLEBOOK['host']:
            return HindlebookPublicPostsRequest(host)
        elif host == DEV_HINDLEBOOK['host']:
            return DevHindlebookPublicPostsRequest(host)
        else:
            raise NotImplementedError('host `%s` does not have a corresponding factory.' % host)

    create = staticmethod(create)


class HindlebookFriendRequest(FriendRequestFactory):
    """
    Hindlebook specific FriendRequest
    """
    def __init__(self, host):
        self.host = host
        self.url = "http://%s/api/friendrequest" % host
        self.auth = HTTPBasicAuth(HINDLEBOOK['username'], HINDLEBOOK['password'])

    def post(self, author, friend):
        data = {"query": "friendrequest",
                "author": AuthorSerializer(author).data,
                "friend": AuthorSerializer(friend).data}
        return requests.post(url=self.url, data=data, auth=self.auth)


class DevHindlebookFriendRequest(FriendRequestFactory):
    """
    Dev_Hindlebook specific FriendRequest
    """
    def __init__(self, host):
        self.host = host
        self.url = "http://%s/api/friendrequest" % host
        self.auth = HTTPBasicAuth(DEV_HINDLEBOOK['username'], DEV_HINDLEBOOK['password'])

    def post(self, author, friend):
        data = {"query": "friendrequest",
                "author": AuthorSerializer(author).data,
                "friend": AuthorSerializer(friend).data}
        return requests.post(url=self.url, data=data, auth=self.auth)
