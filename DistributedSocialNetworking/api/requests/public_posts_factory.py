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
    'username': "hindlebook.tamarabyte.com",
    'password': "test",
    'port': ''
}


class PublicPostsRequestFactory():
    """
    An Encapsulation for building Public Post requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    # Static Factory
    def create(host):
        if host == HINDLEBOOK['host']:
            return HindlebookPublicPostsRequest(host)
        elif host == DEV_HINDLEBOOK['host']:
            return DevHindlebookPublicPostsRequest(host)
        else:
            raise NotImplementedError('host `%s` does not have a corresponding factory.' % host)

    create = staticmethod(create)


class HindlebookPublicPostsRequest(PublicPostsRequestFactory):
    """
    Hindlebook specific Public Post Request
    """
    def __init__(self, host):
        self.host = host
        self.url = "http://%s/api/posts" % host
        self.auth = HTTPBasicAuth(HINDLEBOOK['username'], HINDLEBOOK['password'])

    def get(self):
        return requests.get(url=self.url, auth=self.auth)


class DevHindlebookPublicPostsRequest(PublicPostsRequestFactory):
    """
    Dev_Hindlebook specific Public Post Request
    """
    def __init__(self, host):
        self.host = host
        self.url = "http://%s/api/posts" % host
        self.auth = HTTPBasicAuth(DEV_HINDLEBOOK['username'], DEV_HINDLEBOOK['password'])

    def get(self):
        return requests.get(url=self.url, auth=self.auth)
