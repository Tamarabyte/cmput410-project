from requests.auth import HTTPBasicAuth
from api.serializers import AuthorSerializer
import requests


class FriendRequestFactory():
    """
    An Encapsulation for building FriendRequests
    """
    def post(self):
        raise NotImplementedError('`post()` must be implemented.')

    # Static Factory
    def create(node):
        if node.team_number == 9:
            return HindlebookAuthoredPostsRequest(node)
        else:
            raise NotImplementedError('node `%s` does not have a corresponding factory.' % node.host_name)

    create = staticmethod(create)


class HindlebookFriendRequest(FriendRequestFactory):
    """
    Hindlebook specific FriendRequest
    """
    def __init__(self, node):
        self.node = node
        self.url = "http://%s/api/friendrequest" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def post(self, author, friend):
        data = {"query": "friendrequest",
                "author": AuthorSerializer(author).data,
                "friend": AuthorSerializer(friend).data}
        return requests.post(url=self.url, data=data, auth=self.auth)
