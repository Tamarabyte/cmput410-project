from requests.auth import HTTPBasicAuth
import requests


class ProfileRequestFactory():
    """
    An Encapsulation for building Authored Post requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    # Static Factory
    def create(node):
        if node.team_number == 9:
            return HindlebookAuthoredPostsRequest(node)
        else:
            raise NotImplementedError('node `%s` does not have a corresponding factory.' % node.host_name)

    create = staticmethod(create)


class HindlebookProfileRequest(ProfileRequestFactory):
    """
    Hindlebook specific Authored Post Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "http://%s/api/author" % node.host
        self.auth = HTTPBasicAuth(node.host_name, node.password)

    def get(self, author_uuid):
        self.url = self.url + "/%s" % author_uuid
        return requests.get(url=self.url, auth=self.auth)
