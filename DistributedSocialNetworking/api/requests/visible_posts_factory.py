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
        if node.team_number == 5:
            return SocshizzleVisiblePostsRequest(node)
        if node.team_number == 8:
            return Team8VisiblePostRequest(node)
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
        self.url = "%s/author/posts" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, uuid):
        headers = {'uuid': uuid}
        return requests.get(url=self.url, headers=headers, auth=self.auth)


class Team8VisiblePostRequest(VisiblePostsRequestFactory):
    """
    Team 8 specific Visible Post Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/author/posts" % node.host

    def get(self, uuid, requester_uuid="YourAuthSucks"):
        self.auth = HTTPBasicAuth("%s:%s" % (requester_uuid, self.node.our_username), self.node.our_password)
        # headers = {'uuid': uuid}
        return requests.get(url=self.url, auth=self.auth)


class SocshizzleVisiblePostsRequest(VisiblePostsRequestFactory):
    """
    Hindlebook specific Visible Post Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/posts" % node.host # Just get the public cause their apis fucky
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, uuid):
        return requests.get(url=self.url, auth=self.auth)
