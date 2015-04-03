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

        # Dummy nodes to test authentication
        self.node1 = mommy.make(Node, host='http://test.com', host_name='test', password='test',
                                is_connected=False, team_number=9)
        self.node2 = mommy.make(Node, host='http://node2.com', host_name='node2', password='node2',
                                is_connected=False, team_number=9)

        # Create Users
        self.user1 = mommy.make(User)
        self.user2 = mommy.make(User)
        self.user3 = mommy.make(User)

        # Create authors
        self.author1 = mommy.make(Author, node=self.node1, user=self.user1)
        self.author2 = mommy.make(Author, node=self.node1, user=self.user2)
        self.author3 = mommy.make(Author, node=self.node1, user=self.user3)

        # Create posts
        self.post1 = mommy.make(Post, author=self.author1, title='Post by author1')
        self.post2 = mommy.make(Post, author=self.author2, title='Post by author2')

        # Serialize the authors
        self.author1Data = AuthorSerializer(self.author1)
        self.author2Data = AuthorSerializer(self.author2)

        # Set credentials for Node 1
        # If you change test/test above, this will break... lol. b64encode would not work so I hardcoded
        # Note: since a node is logged in, we implicitly trust it, and assume correct user is making the requests
        self.client.credentials(HTTP_AUTHORIZATION='Basic dGVzdDp0ZXN0',
                                HTTP_UUID="%s" % self.author1.uuid)

    def testFriend2FriendGetQuerySuccess(self):
        """
        Test GET friend2friend query
        api method: service/api/friends/{AUTHOR1_UUID}/{AUTHOR2_UUID}
        """

        # Set authors to be friends
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
        Test POST friend query with one friend in list
        api method: service/api/friends/{AUTHOR_UUID}
        """
        # The uuid of the authors
        id1 = str(self.author1.uuid)
        id2 = str(self.author2.uuid)

        # Set authors to be friends
        self.author1.friends.add(self.author2)
        self.author2.friends.add(self.author1)

        # Some uuids of unknown authors
        fakeUUID = str(uuid_import.uuid4())
        fakeUUID2 = str(uuid_import.uuid4())

        # JSON request with some non-friend uuids
        JSONdata = json.dumps({"query": "friends", "author": id1, "authors": [fakeUUID, id2, fakeUUID2]})

        # POST request for friend querying
        response = self.client.post('/api/friends/%s' % id1, data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        decoded = json.loads(response.content.decode('utf-8'))

        # Ensure the response only includes the real friend
        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['author'], id1, "Author has incorrect ID")
        self.assertEquals(len(decoded['friends']), 1, "Author should have exactly one friend")
        self.assertEquals(decoded['friends'][0], id2, "Authors are not friends but they should be")

    def testFriendRequestSuccess(self):
        """
        Test POST bidirectional friend requests
        api method: service/api/friendrequest
        """
        # JSON format for a friend request
        JSONdata = JSONdata = json.dumps({"query": "friendrequest", "author": self.author1Data.data, "friend": self.author2Data.data})

        # POST request with the json
        response = self.client.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        # The server should return 200
        self.assertEquals(response.status_code, 200, "Response not 200")

        # Author 1 has sent one friend request
        self.assertQuerysetEqual(self.author1.getUnacceptedFriends(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.getUnacceptedFriends(), [])

        # JSON format for the symmetrical request
        JSONdata = JSONdata = json.dumps({"query": "friendrequest", "author": self.author2Data.data, "friend": self.author1Data.data})

        # POST the symmetrical request
        response = self.client.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        # They both have sent a request, they are 'true' friends
        self.assertQuerysetEqual(self.author1.getFriends(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.getFriends(), ["<Author: %s>" % self.author1.username])

    def testFriendRequestRepeated(self):
        """
        Test POST a friend request multiple times
        api method: service/api/friendrequest
        """
        # Send the same friend request multiple times
        for i in range(0, 3):
            # JSON format for a friend request
            JSONdata = json.dumps({"query": "friendrequest", "author": self.author1Data.data, "friend": self.author2Data.data})

            # POST request with the json
            response = self.client.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

            self.assertEquals(response.status_code, 200, "Response not 200")

            # Make sure author1 doesn't try to add author2 more than once
            self.assertEqual(len(self.author1.friends.all()), 1)
            self.assertQuerysetEqual(self.author1.getUnacceptedFriends(), ["<Author: %s>" % self.author2.username])
            self.assertQuerysetEqual(self.author2.getUnacceptedFriends(), [])

    def testFriendRequestFollows(self):
        """
        Test POST a friend request will follow that person
        api method: service/api/friendrequest
        """
        # JSON format for friend request
        JSONdata = json.dumps({"query": "friendrequest", "author": self.author1Data.data, "friend": self.author2Data.data})

        # POST request with json
        response = self.client.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        # Make sure sending a friend request will also follow that author
        self.assertQuerysetEqual(self.author1.follows.all(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.follows.all(), [])

    def testFriendRequestFriendNotFound(self):
        """
        Test POST a friend request from local author to unknown author
        api method: service/api/friendrequest
        """
        # A fake UUID that doesn't exist in our db
        fakeUUID = str(uuid_import.uuid4())
        self.author2.uuid = fakeUUID
        foreignAuthor = AuthorSerializer(self.author2)

        # The JSON with valid author, unknown friend
        JSONdata = {"query": "friendrequest", "author": self.author1Data.data, "friend": foreignAuthor.data}
        response = self.client.post('/api/friendrequest', JSONdata, format='json')

        # The server should return 400 if it can't find the correct friend
        self.assertEquals(response.status_code, 400, "Response should be 400")

    def testFriendRequestAuthorNotFound(self):
        """
        Test POST a friend request from an unknown author to a local author
        api method: service/api/friendrequest
        """
        # Form a user with a UUID that doesn't exist in our db
        fakeUUID = str(uuid_import.uuid4())
        self.author2.uuid = fakeUUID
        foreignAuthor = AuthorSerializer(self.author2)

        # The JSON with unknown author, valid friend
        JSONdata = {"query": "friendrequest", "author": foreignAuthor.data, "friend": self.author1Data.data}
        response = self.client.post('/api/friendrequest', JSONdata, format='json')

        # The server should return 400 if it can't find the correct friend
        self.assertEquals(response.status_code, 400, "Response should be 400")

    def testFriendRequestFromUnknownNode(self):
        """
        Test POST a friend request from unknown node
        api method: service/api/friendrequest
        """
        # Set wrong credentials
        self.client.credentials(HTTP_AUTHORIZATION='Basic ZmFrZTpmYWtl',
                                HTTP_UUID="%s" % self.author1.uuid)

        # POST request with the JSON
        JSONdata = {"query": "friendrequest", "author": self.author2Data.data, "friend": self.author1Data.data}
        response = self.client.post('/api/friendrequest', JSONdata, format='json')

        # The server should return 401 since we're not logged in with correct node credentials
        self.assertEquals(response.status_code, 401, "Response should be 401")

    def testUnfriendRequestFail(self):
        """
        Test POST an unfriend request from another node, which is unauthorized
        api method: service/api/unfriend
        """
        # Set authors to be friends
        self.author1.friends.add(self.author2)
        self.author2.friends.add(self.author1)

        # POST request with the json
        JSONdata = {"query": "friendrequest", "author": self.author2Data.data, "friend": self.author1Data.data}
        response = self.client.post('/api/unfriend', JSONdata, format='json')

        self.assertEquals(response.status_code, 403, "Response should be 403")

    def testFollowRequestSuccess(self):
        """
        Test POST a follow request from another node, which is unauthorized
        api method: service/api/follow
        """
        # POST request with the json
        JSONdata = {"query": "friendrequest", "author": self.author1Data.data, "friend": self.author2Data.data}
        response = self.client.post('/api/follow', JSONdata, format='json')

        self.assertEquals(response.status_code, 403, "Response should be 403")

    def testUnfollowRequestFail(self):
        """
        Test POST an unfollow request from another node, which is unauthorized
        api method: service/api/unfollow
        """
        # Set author 1 to follow author 2
        self.author1.friends.add(self.author2)

        # POST request with the json
        JSONdata = {"query": "friendrequest", "author": self.author1Data.data, "friend": self.author2Data.data}
        response = self.client.post('/api/unfollow', JSONdata, format='json')

        self.assertEquals(response.status_code, 403, "Response should be 403")
