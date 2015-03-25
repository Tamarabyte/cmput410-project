from api.requests import HINDLEBOOK, DEV_HINDLEBOOK
from requests.auth import HTTPBasicAuth
import requests


class VisiblePostsRequestFactory():
    """
    An Encapsulation for building Visible Post requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    # Static Factory
    def create(host):
        if host == HINDLEBOOK['host']:
            return HindlebookVisiblePostsRequest(host)
        elif host == DEV_HINDLEBOOK['host']:
            return DevHindlebookVisiblePostsRequest(host)
        else:
            raise NotImplementedError('host `%s` does not have a corresponding factory.' % host)

    create = staticmethod(create)


class HindlebookVisiblePostsRequest(VisiblePostsRequestFactory):
    """
    Hindlebook specific Visible Post Request
    """
    def __init__(self, host, uuid):
        self.host = host
        self.url = "http://%s/api/author/posts" % host
        self.auth = HTTPBasicAuth(HINDLEBOOK['username'], HINDLEBOOK['password'])

    def get(self, uuid):
        headers = {'uuid': uuid}
        return requests.get(url=self.url, headers=headers, auth=self.auth)


class DevHindlebookVisiblePostsRequest(VisiblePostsRequestFactory):
    """
    Dev_Hindlebook specific Visible Post Request
    """
    def __init__(self, host, uuid):
        self.host = host
        self.url = "http://%s/api/author/posts" % host
        self.auth = HTTPBasicAuth(DEV_HINDLEBOOK['username'], DEV_HINDLEBOOK['password'])

    def get(self, uuid):
        headers = {'uuid': uuid}
        return requests.get(url=self.url, headers=headers, auth=self.auth)
