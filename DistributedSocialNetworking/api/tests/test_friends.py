from django.test import TestCase, Client
from rest_framework.test import  APITestCase
from Hindlebook.models import User, Post
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
        self.author1 = mommy.make(User)
        self.author2 = mommy.make(User)
        self.author3 = mommy.make(User)

        self.post1 = mommy.make(Post)
        self.post2 = mommy.make(Post)

    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()

    # def testFriend2FriendGetQuerySuccess(self):
    #     """ Test a successful friend2friend query """

    #     self.author1.follows.add(self.author2)
    #     self.author2.follows.add(self.author1)

    #     response = c.get('/api/friends/%s/%s' % (self.author1.uuid, self.author2.uuid))

    #     self.assertEquals(response.status_code, 200, "Response not 200")

    #     decoded = json.loads(response.content.decode('utf-8'))

    #     self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
    #     self.assertEquals(decoded['authors'][0], str(self.author1.uuid), "First author has incorrect ID")
    #     self.assertEquals(decoded['authors'][1], str(self.author2.uuid), "Second author has incorrect ID")
    #     self.assertEquals(decoded['friends'], "YES", "Authors are not friends but should be")

    # def testFriendQueryPostSuccessOneFriend(self):
    #     """ Test a successful friend query with one friend in list """

    #     id1 = str(self.author1.uuid)
    #     id2 = str(self.author2.uuid)

    #     self.author1.follows.add(self.author2)
    #     self.author2.follows.add(self.author1)

    #     JSONdata = json.dumps({"query": "friends", "author": id1, "authors": [5, 6, 7, id2, 3]})

    #     response = c.post('/api/friends/%s' % id1,user=self.author1, data=JSONdata, content_type='application/json; charset=utf')

    #     self.assertEquals(response.status_code, 200, "Response not 200")

    #     decoded = json.loads(response.content.decode('utf-8'))

    #     self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
    #     self.assertEquals(decoded['author'], id1, "Author has incorrect ID")
    #     self.assertEquals(len(decoded['friends']), 1, "Author should have exactly one friend")
    #     self.assertEquals(decoded['friends'][0], id2, "Authors are not friends but they should be")

    # def testFriendRequestSuccess(self):
    #     """ Test sending a successful bidirectional friend request """

    #     authorID1 = str(self.author1.uuid)
    #     authorID2 = str(self.author2.uuid)

    #     JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID1, "host": "http://127.0.0.1:8000/", "displayname": "Author1"},
    #                            "friend": {"id": authorID2, "host": "http://127.0.0.1:8000/", "displayname": "Author2",
    #                                       "url": "http://127.0.0.1:8000/author/"+authorID2}})
    #     c.login_user(self.author1)
    #     response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

    #     self.assertEquals(response.status_code, 200, "Response not 200")

    #     self.assertTrue(self.author2 in self.author1.follows.all())
    #     self.assertTrue(len(self.author1.follows.all()) == 1)

    #     self.assertFalse(self.author1 in self.author2.follows.all())
    #     self.assertTrue(len(self.author2.follows.all()) == 0)

    #     JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID2, "host": "http://127.0.0.1:8000/", "displayname": "Author2"},
    #                            "friend": {"id": authorID1, "host": "http://127.0.0.1:8000/", "displayname": "Author1",
    #                                       "url": "http://127.0.0.1:8000/author/"+authorID1}})
    #     c.login_user(self.author2)
    #     response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

    #     self.assertEquals(response.status_code, 200, "Response not 200")

    #     self.assertTrue(self.author2 in self.author1.follows.all())
    #     self.assertTrue(len(self.author1.follows.all()) == 1)

    #     self.assertTrue(self.author1 in self.author2.follows.all())
    #     self.assertTrue(len(self.author2.follows.all()) == 1)

    def testIllegalFriendRequest(self):
        """ Test sending a friend request from the not currently logged in user """
        authorID1 = str(self.author1.uuid)
        authorID2 = str(self.author2.uuid)
        JSONdata = JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID1, "host": "http://127.0.0.1:8000/", "displayname": "Author1"},
                               "friend": {"id": authorID2, "host": "http://127.0.0.1:8000/", "displayname": "Author2",
                                          "url": "http://127.0.0.1:8000/author/"+authorID2}})
        c.login_user(self.author2)
        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')
        self.assertEquals(response.status_code, 200, "Response not 200")

