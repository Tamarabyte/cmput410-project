from requests.auth import HTTPBasicAuth
import requests

import api.serializers

class CommentRequestFactory():
    """
    An Encapsulation for building Public Post requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    # Static Factory
    def create(node):
        if node.team_number == 5:
            return SocshizzleCommentRequest(node)
        if node.team_number == 8:
            return Team8CommentRequest(node)
        if node.team_number == 9:
            return HindlebookCommentRequest(node)
        else:
            raise NotImplementedError('node `%s` does not have a corresponding factory.' % node.host_name)

    create = staticmethod(create)


class Team8CommentRequest(CommentRequestFactory):
    """
    Team 8 specific Public Post Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/api/posts" % node.host

    def post(self,comment, requester_uuid="YourAuthSucks"):
        self.auth = (requester_uuid+":"+self.node.our_username,self.node.our_password)
        self.url = "%s/posts/%s/comment" % (self.node.host, comment.post.guid)
        self.data = api.serializers.CommentSerializer(comment).data
        return requests.post(url=self.url, data=self.data, auth=self.auth)

