# from api.requests import HINDLEBOOK, DEV_HINDLEBOOK, TEST
from requests.auth import HTTPBasicAuth
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


class AuthoredPostsRequestFactory():
    """
    An Encapsulation for building Authored Post requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    # Static Factory
    def create(host, requester_uuid, author_uuid):
        if host == HINDLEBOOK['host']:
            return HindlebookAuthoredPostsRequest(host, requester_uuid, author_uuid)
        elif host == DEV_HINDLEBOOK['host']:
            return DevHindlebookAuthoredPostsRequest(host, requester_uuid, author_uuid)
        else:
            raise NotImplementedError('host `%s` does not have a corresponding factory.' % host)

    create = staticmethod(create)


class HindlebookAuthoredPostsRequest(AuthoredPostsRequestFactory):
    """
    Hindlebook specific Authored Post Request
    """
    def __init__(self, host, requester_uuid, author_uuid):
        self.host = host
        self.url = "http://%s/api/author/%s/posts" % (host, author_uuid)
        self.headers = {'uuid': requester_uuid}
        self.auth = HTTPBasicAuth(HINDLEBOOK['username'], HINDLEBOOK['password'])

    def get(self):
        return requests.get(url=self.url, headers=self.headers, auth=self.auth)


class DevHindlebookAuthoredPostsRequest(AuthoredPostsRequestFactory):
    """
    Dev_Hindlebook specific Authored Post Request
    """
    def __init__(self, host, requester_uuid, author_uuid):
        self.host = host
        self.url = "http://%s/api/author/%s/posts" % (host, author_uuid)
        self.headers = {'uuid': requester_uuid}
        self.auth = HTTPBasicAuth(DEV_HINDLEBOOK['username'], DEV_HINDLEBOOK['password'])

    def get(self):
        return requests.get(url=self.url, headers=self.headers, auth=self.auth)
