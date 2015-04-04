from requests.auth import HTTPBasicAuth
import requests



class PostRequestFactory():
    """
    An Encapsulation for building GET/PUT/POST Post requests
    """
    def get(self):
        raise NotImplementedError('`get()` must be implemented.')

    def post(self):
        raise NotImplementedError('`post()` must be implemented.')

    def put(self):
        raise NotImplementedError('`put()` must be implemented.')

    # Static Factory
    def create(node):
        if node.team_number == 5:
            return SocshizzlePostRequest(node)
        if node.team_number == 8:
            return Team8PostRequest(node)
        if node.team_number == 9:
            return HindlebookPostRequest(node)
        else:
            raise NotImplementedError('node `%s` does not have a corresponding factory.' % node.host_name)

    create = staticmethod(create)


class HindlebookPostRequest(PostRequestFactory):
    """
    Hindlebook specific GET/PUT/POST Post requests
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/api/post" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, post_id):
        self.url = self.url + "/%s" % post_id
        return requests.get(url=self.url, auth=self.auth)

    def post(self, post_id, serializedPost):
        self.url = self.url + "/%s" % post_id
        return requests.post(url=self.url, data=serializedPost, auth=self.auth)

    def put(self, post_id, serializedPost):
        self.url = self.url + "/%s" % post_id
        return requests.put(url=self.url, data=serializedPost, auth=self.auth)


class Team8PostRequest(PostRequestFactory):
    """
    Team 8 specific GET/PUT/POST Post requests
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/post" % node.host

    def get(self, post_id, requester_uuid="YourAuthSucks"):
        self.auth = (requester_uuid+":"+self.node.our_username,self.node.our_password)
        self.url = self.url + "/%s" % post_id
        return requests.get(url=self.url, auth=self.auth)

    def post(self, post_id, serializedPost, requester_uuid="YourAuthSucks"):
        self.auth = (requester_uuid+":"+self.node.our_username,self.node.our_password)
        self.url = self.url + "/%s" % post_id
        return requests.post(url=self.url, data=serializedPost, auth=self.auth)

    def put(self, post_id, serializedPost, requester_uuid="YourAuthSucks"):
        self.auth = (requester_uuid+":"+self.node.our_username,self.node.our_password)
        self.url = self.url + "/%s" % post_id
        return requests.put(url=self.url, data=serializedPost, auth=self.auth)


class SocshizzlePostRequest(PostRequestFactory):
    """
    Socshizzle specific GET/PUT/POST Post requests
    """
    def __init__(self, node):
        self.node = node
        self.url = "%s/post" % node.host
        self.auth = HTTPBasicAuth(node.our_username, node.our_password)

    def get(self, post_id):
        self.url = self.url + "/%s" % post_id
        return requests.get(url=self.url, auth=self.auth)

    def post(self, post_id, serializedPost):
        self.url = self.url + "/%s" % post_id
        return requests.post(url=self.url, data=serializedPost, auth=self.auth)

    def put(self, post_id, serializedPost):
        self.url = self.url + "/%s" % post_id
        return requests.put(url=self.url, data=serializedPost, auth=self.auth)
