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


class PostRequestFactory():
    """
    An Encapsulation for building GET/PUT/POST Post requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    def post(self):
        raise NotImplementedError('`post()` must be implemented.')

    def put(self):
        raise NotImplementedError('`put()` must be implemented.')

    # Static Factory
    def create(host, post_id):
        if host == HINDLEBOOK['host']:
            return HindlebookAuthoredPostsRequest(host, post_id)
        elif host == DEV_HINDLEBOOK['host']:
            return DevHindlebookAuthoredPostsRequest(host, post_id)
        else:
            raise NotImplementedError('host `%s` does not have a corresponding factory.' % host)

    create = staticmethod(create)


class HindlebookPostRequest(AuthoredPostsRequestFactory):
    """
    Hindlebook specific GET/PUT/POST Post requests
    """
    def __init__(self, host, post_id):
        self.host = host
        self.url = "http://%s/api/post/%s" % (host, post_id)
        self.auth = HTTPBasicAuth(HINDLEBOOK['username'], HINDLEBOOK['password'])

    def get(self):
        return requests.get(url=self.url, auth=self.auth)

    def post(self, data):
        return requests.post(url=self.url, data=data, auth=self.auth)

    def put(self, data):
        return requests.put(url=self.url, data=data, auth=self.auth)


class DevHindlebookPostRequest(AuthoredPostsRequestFactory):
    """
    Dev_Hindlebook specific GET/PUT/POST Post requests
    """
    def __init__(self, host, post_id):
        self.host = host
        self.url = "http://%s/api/post/%s" % (host, post_id)
        self.auth = HTTPBasicAuth(DEV_HINDLEBOOK['username'], DEV_HINDLEBOOK['password'])

    def get(self):
        return requests.get(url=self.url, auth=self.auth)

    def post(self, data):
        return requests.post(url=self.url, data=data, auth=self.auth)

    def put(self, data):
        return requests.put(url=self.url, data=data, auth=self.auth)
