from api.requests import HINDLEBOOK, DEV_HINDLEBOOK
from requests.auth import HTTPBasicAuth
import requests


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
    def create(host):
        if host == HINDLEBOOK['host']:
            return HindlebookAuthoredPostsRequest(host)
        elif host == DEV_HINDLEBOOK['host']:
            return DevHindlebookAuthoredPostsRequest(host)
        else:
            raise NotImplementedError('host `%s` does not have a corresponding factory.' % host)

    create = staticmethod(create)


class HindlebookPostRequest(PostRequestFactory):
    """
    Hindlebook specific GET/PUT/POST Post requests
    """
    def __init__(self, host):
        self.host = host
        self.url = "http://%s/api/post" % host
        self.auth = HTTPBasicAuth(HINDLEBOOK['username'], HINDLEBOOK['password'])

    def get(self, post_id):
        self.url = self.url + "/%s" % post_id
        return requests.get(url=self.url, auth=self.auth)

    def post(self, post_id, post):
        self.url = self.url + "/%s" % post_id
        data = PostSerializer(post).data
        return requests.post(url=self.url, data=data, auth=self.auth)

    def put(self, post_id, post):
        self.url = self.url + "/%s" % post_id
        data = PostSerializer(post).data
        return requests.put(url=self.url, data=data, auth=self.auth)


class DevHindlebookPostRequest(PostRequestFactory):
    """
    Dev_Hindlebook specific GET/PUT/POST Post requests
    """
    def __init__(self, host):
        self.host = host
        self.url = "http://%s/api/post/%s" % (host, post_id)
        self.auth = HTTPBasicAuth(DEV_HINDLEBOOK['username'], DEV_HINDLEBOOK['password'])

    def get(self, post_id):
        self.url = self.url + "/%s" % post_id
        return requests.get(url=self.url, auth=self.auth)

    def post(self, post_id, post):
        self.url = self.url + "/%s" % post_id
        data = PostSerializer(post).data
        return requests.post(url=self.url, data=data, auth=self.auth)

    def put(self, post_id, post):
        self.url = self.url + "/%s" % post_id
        data = PostSerializer(post).data
        return requests.put(url=self.url, data=data, auth=self.auth)
