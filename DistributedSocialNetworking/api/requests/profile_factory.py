from requests.auth import HTTPBasicAuth
import requests


class ProfileRequestFactory():
    """
    An Encapsulation for building Profile Requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    # Static Factory
    def create(node):
        if node.team_number == 5:
            return SocshizzleProfileRequest(node)
        if node.team_number == 8:
            return Team8ProfileRequest(node)
        if node.team_number == 9:
            return HindlebookProfileRequest(node)
        else:
            raise NotImplementedError('node `%s` does not have a corresponding factory.' % node.host_name)

    create = staticmethod(create)


class HindlebookProfileRequest(ProfileRequestFactory):
    """
    Hindlebook specific Profile Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/author" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, author_uuid):
        self.url = self.url + "/%s" % author_uuid
        return requests.get(url=self.url, auth=self.auth)


class Team8ProfileRequest(ProfileRequestFactory):
    """
    Team 8 specific Profile Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/friends" % node.host

    def get(self, author_uuid, requester_uuid="YourAuthSucks"):
        self.auth = HTTPBasicAuth("%s:%s" % (requester_uuid, self.node.our_username) , self.node.our_password)
        self.url = self.url + "/%s" % author_uuid
        return requests.get(url=self.url, auth=self.auth)


class SocshizzleProfileRequest(ProfileRequestFactory):
    """
    Socshizzle specific Profile Request
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/author" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, author_uuid):
        self.url = self.url + "/%s" % author_uuid
        return requests.get(url=self.url, auth=self.auth)
