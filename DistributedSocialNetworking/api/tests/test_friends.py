from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from Hindlebook.models import Author, Post
from api.testclient import TestClient, APITestClient
from api.serializers.post_serializer import PostSerializer
from model_mommy import mommy
from django.utils.six import BytesIO
from rest_framework import status
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest
import json
import base64
import uuid as uuid_import

c = TestClient()
client = APITestClient()
server = "http://localhost:8000"


class APITests(APITestCase):
    """ Test some of the GET/POST API """

    def setUp(self):
        self.user1 = mommy.make(User)
        self.user2 = mommy.make(User)
        self.user3 = mommy.make(User)

        self.author1 = mommy.make(Author, user=self.user1)
        self.author2 = mommy.make(Author, user=self.user2)
        self.author3 = mommy.make(Author, user=self.user3)

        self.post1 = mommy.make(Post, author=self.author1)
        self.post2 = mommy.make(Post, author=self.author2)

    def testFriend2FriendGetQuerySuccess(self):
        """ Test a successful friend2friend query """

        self.author1.friends.add(self.author2)
        self.author2.friends.add(self.author1)

        response = c.get('/api/friends/%s/%s' % (self.author1.uuid, self.author2.uuid))

        self.assertEquals(response.status_code, 200, "Response not 200")

        decoded = json.loads(response.content.decode('utf-8'))

        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['authors'][0], str(self.author1.uuid), "First author has incorrect ID")
        self.assertEquals(decoded['authors'][1], str(self.author2.uuid), "Second author has incorrect ID")
        self.assertEquals(decoded['friends'], "YES", "Authors are not friends but should be")

    def testFriendQueryPostSuccessOneFriend(self):
        """ Test a successful friend query with one friend in list """

        id1 = str(self.author1.uuid)
        id2 = str(self.author2.uuid)

        self.author1.friends.add(self.author2)
        self.author2.friends.add(self.author1)

        fakeUUID = str(uuid_import.uuid4())
        fakeUUID2 = str(uuid_import.uuid4())

        JSONdata = json.dumps({"query": "friends", "author": id1, "authors": [fakeUUID, id2, fakeUUID2]})

        response = c.post('/api/friends/%s' % id1, user=self.author1, data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        decoded = json.loads(response.content.decode('utf-8'))

        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['author'], id1, "Author has incorrect ID")
        self.assertEquals(len(decoded['friends']), 1, "Author should have exactly one friend")
        self.assertEquals(decoded['friends'][0], id2, "Authors are not friends but they should be")

    def testFriendRequestSuccess(self):
        """ Test sending a successful bidirectional friend request """

        authorID1 = str(self.author1.uuid)
        authorID2 = str(self.author2.uuid)

        JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID1, "host": server, "displayname": self.author1.username},
                               "friend": {"id": authorID2, "host": server, "displayname": self.author2.username,
                                          "url": server + "/author/" + authorID2}})
        c.login_user(self.author1.user)

        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        self.assertQuerysetEqual(self.author1.getUnacceptedFriends(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.getUnacceptedFriends(), [])

        JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID2, "host": server, "displayname": self.author2.username},
                               "friend": {"id": authorID1, "host": server, "displayname": self.author1.username,
                                          "url": server + "/author/" + authorID1}})
        c.login_user(self.author2.user)
        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        self.assertQuerysetEqual(self.author1.getFriends(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.getFriends(), ["<Author: %s>" % self.author1.username])

    def testFriendRequestRepeated(self):
        """ Test sending a friend request multiple times """

        authorID1 = str(self.author1.uuid)
        authorID2 = str(self.author2.uuid)

        for i in range(0, 3):
            JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID1, "host": server, "displayname": self.author1.username},
                                   "friend": {"id": authorID2, "host": server, "displayname": self.author2.username,
                                              "url": server + "/author/" + authorID2}})
            c.login_user(self.author1.user)

            response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

            self.assertEquals(response.status_code, 200, "Response not 200")

            self.assertEqual(len(self.author1.friends.all()), 1)
            self.assertQuerysetEqual(self.author1.getUnacceptedFriends(), ["<Author: %s>" % self.author2.username])
            self.assertQuerysetEqual(self.author2.getUnacceptedFriends(), [])

    def testFriendRequestFollows(self):
        """ Test sending a friend request will follow that person """

        authorID1 = str(self.author1.uuid)
        authorID2 = str(self.author2.uuid)

        JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID1, "host": server, "displayname": self.author1.username},
                               "friend": {"id": authorID2, "host": server, "displayname": self.author2.username,
                                          "url": server + "/author/" + authorID2}})
        c.login_user(self.author1.user)

        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        self.assertQuerysetEqual(self.author1.follows.all(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.follows.all(), [])

    def testIllegalFriendRequest(self):
        """ Test sending a friend request from the not currently logged in user """
        authorID1 = str(self.author1.uuid)
        authorID2 = str(self.author2.uuid)
        JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID1, "host": server, "displayname": self.author1.username},
                               "friend": {"id": authorID2, "host": server, "displayname": self.author2.username,
                                          "url": server + "/author/" + authorID2}})
        c.login_user(self.author2.user)
        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        # This should probably be a 403 - Forbidden? If logged in as wrong user?
        self.assertNotEquals(response.status_code, 200, "Response should not be 200 Ok")
