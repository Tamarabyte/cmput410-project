from api.requests import HINDLEBOOK, DEV_HINDLEBOOK
from requests.auth import HTTPBasicAuth
import requests


class ProfileRequestFactory():
    """
    An Encapsulation for building Authored Post requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    # Static Factory
    def create(host):
        if host == HINDLEBOOK['host']:
            return HindlebookProfileRequest(host)
        elif host == DEV_HINDLEBOOK['host']:
            return DevHindlebookProfileRequest(host)
        else:
            raise NotImplementedError('host `%s` does not have a corresponding factory.' % host)

    create = staticmethod(create)


class HindlebookProfileRequest(ProfileRequestFactory):
    """
    Hindlebook specific Authored Post Request
    """
    def __init__(self, host):
        self.host = host
        self.url = "http://%s/api/author" % host
        self.auth = HTTPBasicAuth(HINDLEBOOK['username'], HINDLEBOOK['password'])

    def get(self, author_uuid):
        self.url = self.url + "/%s" % author_uuid
        return requests.get(url=self.url, auth=self.auth)


class DevHindlebookProfileRequest(ProfileRequestFactory):
    """
    Dev_Hindlebook specific Authored Post Request
    """
    def __init__(self, host):
        self.host = host
        self.url = "http://%s/api/author" % host
        self.auth = HTTPBasicAuth(DEV_HINDLEBOOK['username'], DEV_HINDLEBOOK['password'])

    def get(self, author_uuid):
        self.url = self.url + "/%s" % author_uuid

        return requests.get(url=self.url, auth=self.auth)
