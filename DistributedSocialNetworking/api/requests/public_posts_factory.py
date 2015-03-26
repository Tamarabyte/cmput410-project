from requests.auth import HTTPBasicAuth
import requests


class PublicPostsRequestFactory():
    """
    An Encapsulation for building Public Post requests
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


class HindlebookPublicPostsRequest(PublicPostsRequestFactory):
    """
    Hindlebook specific Public Post Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "http://%s/api/posts" % node.host
        self.auth = HTTPBasicAuth(node.host_name, node.password)

    def get(self):
        return requests.get(url=self.url, auth=self.auth)
