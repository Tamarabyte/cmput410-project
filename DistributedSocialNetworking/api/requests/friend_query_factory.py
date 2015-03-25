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
    'username': "hindlebook.tamarabyte.com",
    'password': "test",
    'port': ''
}


class FriendQueryRequestFactory():
    """
    An Encapsulation for building Author to Author friend querying
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

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


class HindlebookFriendQueryRequest(FriendQueryRequestFactory):
    """
    Hindlebook specific FriendRequest
    """
    def __init__(self, host):
        self.host = host
        self.url = "http://%s/api/friends" % host
        self.auth = HTTPBasicAuth(HINDLEBOOK['username'], HINDLEBOOK['password'])

    def get(self, uuid1, uuid2):
        self.url = self.url + "/%s/%s" % (uuid1, uuid2)
        return requests.get(url=self.url, auth=self.auth)

    def post(self, uuid, uuids=[]):
        self.url = self.url + "/%s" % uuid
        data = {"query": "friends",
                "author": uuid,
                "authors": uuids}
        return requests.get(url=self.url, data=data, auth=self.auth)


class DevHindlebookFriendQueryRequest(FriendQueryRequestFactory):
    """
    Dev_Hindlebook specific FriendRequest
    """
    def __init__(self, host):
        self.host = host
        self.url = "http://%s/api/friends" % host
        self.auth = HTTPBasicAuth(DEV_HINDLEBOOK['username'], DEV_HINDLEBOOK['password'])

    def get(self, uuid1, uuid2):
        self.url = self.url + "/%s/%s" % (uuid1, uuid2)
        return requests.get(url=self.url, auth=self.auth)

    def post(self, uuid, uuids=[]):
        self.url = self.url + "/%s" % uuid
        data = {"query": "friends",
                "author": uuid,
                "authors": uuids}
        return requests.get(url=self.url, data=data, auth=self.auth)
