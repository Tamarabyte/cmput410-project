from Hindlebook.models import Author, Post, Node
from rest_framework.test import APITestCase, APIClient
from api.serializers import AuthorSerializer
from model_mommy import mommy
from rest_framework import status
import json
import base64
import uuid as uuid_import
from django.contrib.auth import get_user_model

User = get_user_model()


class APITests(APITestCase):
    """
    Test some of the Friends API
    """

    def setUp(self):
        self.client = APIClient()

        # A dummy node to test authentication
        self.node1 = mommy.make(Node, host='http://test.com', host_name='test', password='test', is_connected=False)
        self.node2 = mommy.make(Node, host='http://node2.com', host_name='node2', password='node2', is_connected=False)

        # Create Users
        self.user1 = mommy.make(User)
        self.user2 = mommy.make(User)
        self.user3 = mommy.make(User)

        # Create authors
        self.author1 = mommy.make(Author, node=self.node1, user=self.user1)
        self.author2 = mommy.make(Author, node=self.node1, user=self.user2)
        self.author3 = mommy.make(Author, node=self.node1, user=self.user3)

        # Create posts
        self.post1 = mommy.make(Post, author=self.author1)
        self.post2 = mommy.make(Post, author=self.author2)

        # Set credentials for Node 1
        # If you change test/test above, this will break... lol. b64encode would not work so I hardcoded
        self.client.credentials(HTTP_AUTHORIZATION='Basic dGVzdDp0ZXN0',
                                HTTP_UUID="%s" % self.author1.uuid)

    def testFriend2FriendGetQuerySuccess(self):
        """
        Test a successful friend2friend query
        """

        # Authors are now friends
        self.author1.friends.add(self.author2)
        self.author2.friends.add(self.author1)

        # GET request to query friend2friend
        response = self.client.get('/api/friends/%s/%s' % (self.author1.uuid, self.author2.uuid))

        self.assertEquals(response.status_code, 200, "Response not 200")

        decoded = json.loads(response.content.decode('utf-8'))

        # The response should show that they are friends
        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['authors'][0], str(self.author1.uuid), "First author has incorrect ID")
        self.assertEquals(decoded['authors'][1], str(self.author2.uuid), "Second author has incorrect ID")
        self.assertEquals(decoded['friends'], "YES", "Authors are not friends but should be")

    def testFriendQueryPostSuccessOneFriend(self):
        """
        Test a successful friend query with one friend in list
        """

        id1 = str(self.author1.uuid)
        id2 = str(self.author2.uuid)

        # Set authors to be friends
        self.author1.friends.add(self.author2)
        self.author2.friends.add(self.author1)

        fakeUUID = str(uuid_import.uuid4())
        fakeUUID2 = str(uuid_import.uuid4())

        # Send a query with some non-friend uuids
        JSONdata = json.dumps({"query": "friends", "author": id1, "authors": [fakeUUID, id2, fakeUUID2]})

        # POST request for friend querying
        response = self.client.post('/api/friends/%s' % id1, user=self.author1, data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        decoded = json.loads(response.content.decode('utf-8'))

        # Ensure the response only includes the real friend
        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['author'], id1, "Author has incorrect ID")
        self.assertEquals(len(decoded['friends']), 1, "Author should have exactly one friend")
        self.assertEquals(decoded['friends'][0], id2, "Authors are not friends but they should be")

    def testFriendRequestSuccess(self):
        """
        Test sending a successful bidirectional friend request
        """

        # The serialized format of an author
        author1 = AuthorSerializer(self.author1)
        author2 = AuthorSerializer(self.author2)

        # JSON format for a friend request
        JSONdata = JSONdata = json.dumps({"query": "friendrequest", "author": author1.data, "friend": author2.data})

        # POST request with the json
        response = self.client.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        # Author 1 has sent one friend request
        self.assertQuerysetEqual(self.author1.getUnacceptedFriends(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.getUnacceptedFriends(), [])

        # JSON format for the symmetrical request
        JSONdata = JSONdata = json.dumps({"query": "friendrequest", "author": author2.data, "friend": author1.data})

        # POST the symmetrical request
        response = self.client.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        # They both have sent one request, they are 'true' friends
        self.assertQuerysetEqual(self.author1.getFriends(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.getFriends(), ["<Author: %s>" % self.author1.username])

    def testFriendRequestRepeated(self):
        """
        Test sending a friend request multiple times
        """

        author1 = AuthorSerializer(self.author1)
        author2 = AuthorSerializer(self.author2)

        for i in range(0, 3):
            # JSON format for a friend request
            JSONdata = json.dumps({"query": "friendrequest", "author": author1.data, "friend": author2.data})

            # POST request with the json
            response = self.client.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

            self.assertEquals(response.status_code, 200, "Response not 200")

            # Make sure author1 doesn't try to add author2 more than once
            self.assertEqual(len(self.author1.friends.all()), 1)
            self.assertQuerysetEqual(self.author1.getUnacceptedFriends(), ["<Author: %s>" % self.author2.username])
            self.assertQuerysetEqual(self.author2.getUnacceptedFriends(), [])

    def testFriendRequestFollows(self):
        """
        Test sending a friend request will follow that person
        """

        author1 = AuthorSerializer(self.author1)
        author2 = AuthorSerializer(self.author2)

        # JSON format for friend request
        JSONdata = json.dumps({"query": "friendrequest", "author": author1.data, "friend": author2.data})

        # POST request with json
        response = self.client.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        # Make sure sending a friend request will also follow that author
        self.assertQuerysetEqual(self.author1.follows.all(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.follows.all(), [])

    def testFriendRequestFriendNotFound(self):
        """
        Test sending a friend request from local author to unknown author
        """
        # Friend request from local author
        author1 = AuthorSerializer(self.author1)

        # A fake UUID that doesn't exist in our db
        fakeUUID = str(uuid_import.uuid4())
        self.author2.uuid = fakeUUID
        author2 = AuthorSerializer(self.author2)

        # The JSON with valid author, unknown friend
        JSONdata = {"query": "friendrequest", "author": author1.data, "friend": author2.data}
        response = self.client.post('/api/friendrequest', JSONdata, format='json')

        # The server should return 200
        self.assertEquals(response.status_code, 200, "Response should be 200")

        # Server should have created a foreign author from unknown UUID
        foreignAuthor = Author.objects.get(uuid=fakeUUID)
        self.assertEquals(foreignAuthor.username, self.author2.username, "Created foreign author has wrong name")
        self.assertQuerysetEqual(self.author1.getUnacceptedFriends(), ["<Author: %s>" % foreignAuthor.username])

    def testFriendRequestAuthorNotFound(self):
        """
        Test sending a friend request from an unknown author to a local author
        """
        # Friend request to local author
        author1 = AuthorSerializer(self.author1)

        # Form a user with a UUID that doesn't exist in our db
        fakeUUID = str(uuid_import.uuid4())
        self.author2.uuid = fakeUUID
        author2 = AuthorSerializer(self.author2)

        # The JSON with unknown author, valid friend
        JSONdata = {"query": "friendrequest", "author": author2.data, "friend": author1.data}
        response = self.client.post('/api/friendrequest', JSONdata, format='json')

        # The server should return 200
        self.assertEquals(response.status_code, 200, "Response should be 200")

        # Server should have created a foreign author from unknown UUID
        foreignAuthor = Author.objects.get(uuid=fakeUUID)
        self.assertEquals(foreignAuthor.username, self.author2.username, "Created foreign author has wrong name")
        self.assertQuerysetEqual(foreignAuthor.getUnacceptedFriends(), ["<Author: %s>" % self.author1.username])

    def testFriendRequestFromUnknownNode(self):
        """
        Unkown Hosts should be rejected
        """
        # Friend request to local author
        author1 = AuthorSerializer(self.author1)

        # Form a user with a Node that doesn't exist in our db
        self.author2.node = self.node2
        author2 = AuthorSerializer(self.author2)
        Node.objects.filter(host=self.author2.node).delete()

        # The JSON with unknown author, valid friend
        JSONdata = {"query": "friendrequest", "author": author2.data, "friend": author1.data}
        response = self.client.post('/api/friendrequest', JSONdata, format='json')

        # The server should return 400
        self.assertEquals(response.status_code, 400, "Response should be 400")
