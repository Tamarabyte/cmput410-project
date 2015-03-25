from Hindlebook.models import Author, Post, Node
from rest_framework.test import APITestCase, APIClient
from api.serializers import AuthorSerializer
from model_mommy import mommy
from rest_framework import status
import json
import base64
import uuid as uuid_import


class ApiAuthenticationTests(APITestCase):
    """
    Test Api authentication
    """

    def setUp(self):
        self.client = APIClient()

        # Create authors
        self.author1 = mommy.make(Author)
        self.author2 = mommy.make(Author)
        self.author3 = mommy.make(Author)

        # Create posts
        self.post1 = mommy.make(Post, author=self.author1)
        self.post2 = mommy.make(Post, author=self.author2)

        # A dummy node to test authentication
        self.node1 = mommy.make(Node, host='test', password='test')

        # Set credentials for Node 1
        # If you change test/test above, this will break... lol. b64encode would not work so I hardcoded
        self.client.credentials(HTTP_AUTHORIZATION='Basic dGVzdDp0ZXN0',
                                HTTP_UUID="%s" % self.author1.uuid)

    def testUnathenticatedFriendRequest(self):
        """
        Test sending a friend request not authenticated
        """

        author1 = AuthorSerializer(self.author1)
        author2 = AuthorSerializer(self.author2)

        JSONdata = json.dumps({"query": "friendrequest", "author": author1.data, "friend": author2.data})

        # No longer have valid authentication
        self.client.credentials()

        response = self.client.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        # The server should not let unauthenticated users post friend requests
        self.assertEquals(response.status_code, 401, "Response should be 401")
