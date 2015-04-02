from requests.auth import HTTPBasicAuth
import requests


class AuthoredPostsRequestFactory():
    """
    An Encapsulation for building Authored Post requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    # Static Factory
    def create(node):
        if node.team_number == 5:
            return SocshizzleAuthoredPostsRequest(node)

        if node.team_number == 8:
            return Team8PostsRequest(node)
        if node.team_number == 9:
            return HindlebookAuthoredPostsRequest(node)
        else:
            raise NotImplementedError('node `%s` does not have a corresponding factory.' % node.host_name)

    create = staticmethod(create)


class HindlebookAuthoredPostsRequest(AuthoredPostsRequestFactory):
    """
    Hindlebook specific Authored Post Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/author" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, requester_uuid, author_uuid):
        self.url = self.url + "/%s/posts" % author_uuid
        self.headers = {'uuid': requester_uuid}
        return requests.get(url=self.url, headers=self.headers, auth=self.auth)


class Team8PostRequest(AuthoredPostsRequestFactory):
    """
    Team 8 specific Authored Post Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/author" % node.host

    def get(self, author_uuid, requester_uuid="YourAuthSucks"):
        self.auth = HTTPBasicAuth("%s:%s" % (requester_uuid, self.node.our_username) , self.node.our_password)
        self.url = self.url + "/%s/posts" % author_uuid
        # self.headers = {'uuid': requester_uuid}
        return requests.get(url=self.url, auth=self.auth)


class SocshizzleAuthoredPostsRequest(AuthoredPostsRequestFactory):
    """
    Socshizzle specific Authored Post Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/author" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, requester_uuid, author_uuid):
        self.url = self.url + "/%s/posts" % author_uuid
        return requests.get(url=self.url, auth=self.auth)
