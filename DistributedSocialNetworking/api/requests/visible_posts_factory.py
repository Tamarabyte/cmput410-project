from requests.auth import HTTPBasicAuth
import requests


class VisiblePostsRequestFactory():
    """
    An Encapsulation for building Visible Post requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    # Static Factory
    def create(node):
        if node.team_number == 9:
            return HindlebookVisiblePostsRequest(node)
        else:
            raise NotImplementedError('node `%s` does not have a corresponding factory.' % node.host_name)

    create = staticmethod(create)


class HindlebookVisiblePostsRequest(VisiblePostsRequestFactory):
    """
    Hindlebook specific Visible Post Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "http://%s/api/author/posts" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, uuid):
        headers = {'uuid': uuid}
        return requests.get(url=self.url, headers=headers, auth=self.auth)
