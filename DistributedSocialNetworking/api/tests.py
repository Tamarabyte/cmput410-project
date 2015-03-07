from django.test import TestCase, Client
from Hindlebook.models import User
from model_mommy import mommy
import json

c = Client()


class APITests(TestCase):
    """ Test some of the GET/POST API """

    def setUp(self):
        self.author1 = mommy.make(User)
        self.author2 = mommy.make(User)
        self.author3 = mommy.make(User)

    def tearDown(self):
        User.objects.all().delete()

    def testFriend2FriendGetQuerySuccess(self):
        """ Test a successful friend2friend query """

        # Set the 2 authors to be 'real' friends
        self.author1.follows.add(self.author2)
        self.author2.follows.add(self.author1)

        # Send a GET request to check if they are friends
        response = c.get('/api/friends/%s/%s' % (self.author1.id, self.author2.id))

        # Expects a 200 Ok with a JSON response
        self.assertEquals(response.status_code, 200, "Response not 200")

        # Decode the JSON response
        decoded = json.loads(response.content.decode('utf-8'))

        # Expects a JSON response similar to:
        # https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
        # except hindle's specifies "friends":[id1, id2], and also "friends":"YES", but they shouldn't be the same key name??
        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['authors'][0], str(self.author1.id), "First author has incorrect ID")
        self.assertEquals(decoded['authors'][1], str(self.author2.id), "Second author has incorrect ID")
        self.assertEquals(decoded['friends'], "YES", "Authors are not friends but should be")

    def testFriend2FriendGetQueryFailFirstID(self):
        """ Test a friend2friend query with invalid first author ID """

        # Send a GET request with invalid first author ID
        response = c.get('/api/friend/%s/%s' % (555, self.author2.id))

        # Expects a 404 response
        self.assertEquals(response.status_code, 404, "Response not 404")

    def testFriend2FriendGetQueryFailSecondURL(self):
        """ Test a friend2friend query with invalid second author ID """

        # Send a GET request with invalid second author ID
        response = c.get('/api/friend/%s/%s' % (self.author1.id, 555))

        # Expects a 404 response
        self.assertEquals(response.status_code, 404, "Response not 404")

    def testFriend2FriendGetQueryFailURL(self):
        """ Test a friend2friend query with invalid URL """

        # Send a GET request with wrong URL
        response = c.get('/api/frond/%s/%s' % (self.author1.id, self.author2.id))

        # Expects a 404 response
        self.assertEquals(response.status_code, 404, "Response not 404")

    def testFriendQueryPostSuccessOneFriend(self):
        """ Test a successful friend query with one friend in list """

        # Set the 2 authors to be 'real' friends
        self.author1.follows.add(self.author2)
        self.author2.follows.add(self.author1)

        # JSON specifying a list of authors to check friendship with author1
        JSONdata = json.dumps({"query": "friends", "author": self.author1.id, "authors": [5, 6, 7, self.author2.id, 3]})

        # Send a POST request to check if author1 is friends with anyone in the authors list
        response = c.post('/api/friends/%s' % self.author1.id, data=JSONdata, content_type='application/json; charset=utf')

        # Expects a 200 Ok with a JSON response
        self.assertEquals(response.status_code, 200, "Response not 200")

        # Decode the JSON response
        decoded = json.loads(response.content.decode('utf-8'))

        # Expects a JSON response with these values
        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['author'], str(self.author1.id), "Author has incorrect ID")
        self.assertEquals(len(decoded['friends']), 1, "Author should have exactly one friend")
        self.assertEquals(decoded['friends'][0], self.author2.id, "Authors are not friends but they should be")

    def testFriendQueryPostSuccessNoFriends(self):
        """ Test a successful friend query with zero friends in list """

        # Set the 2 authors to be 'real' friends
        self.author1.follows.add(self.author2)
        self.author2.follows.add(self.author1)

        # JSON specifying a list of authors to check friendship with author1
        JSONdata = json.dumps({"query": "friends", "author": self.author1.id, "authors": [5, 6, 7, 3]})

        # Send a POST request to check if author1 is friends with anyone in the authors list
        response = c.post('/api/friends/%s' % self.author1.id, data=JSONdata, content_type='application/json; charset=utf')

        # Expects a 200 Ok with a JSON response
        self.assertEquals(response.status_code, 200, "Response not 200")

        # Decode the JSON response
        decoded = json.loads(response.content.decode('utf-8'))

        # Expects a JSON response with these values
        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['author'], str(self.author1.id), "Author has incorrect ID")
        self.assertEquals(len(decoded['friends']), 0, "Author should have exactly zero friends")

    def testFriendQueryPostSuccessEmptyRequest(self):
        """ Test a successful friend query with empty list """

        # JSON specifying a list of authors to check friendship with author1
        JSONdata = json.dumps({"query": "friends", "author": self.author1.id, "authors": []})

        # Send a POST request with empty author list
        response = c.post('/api/friends/%s' % self.author1.id, data=JSONdata, content_type='application/json; charset=utf')

        # Expects a 200 Ok with a JSON response
        self.assertEquals(response.status_code, 200, "Response not 200")

        # Decode the JSON response
        decoded = json.loads(response.content.decode('utf-8'))

        # Expects a JSON response with these values
        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['author'], str(self.author1.id), "Author has incorrect ID")
        self.assertEquals(len(decoded['friends']), 0, "Author should have zero friends")

    def testFriendQueryPostFailSyntaxKey(self):
        """ Test a failed friend query with wrong JSON key name """

        # JSON with a wrong key name
        JSONdata = json.dumps({"query": "friends", "person": self.author1.id, "authors": [5, 6, 7, self.author2.id, 3]})

        # Send a POST request with invalid JSON
        response = c.post('/api/friends/%s' % self.author1.id, data=JSONdata, content_type='application/json; charset=utf')

        # Expects a 400 Bad Request
        self.assertEquals(response.status_code, 400, "Response not 400")

    def testFriendQueryPostFailInconsistentID(self):
        """ Test a failed friend query with URL not matching JSON """

        # JSON with a different author value than the URL
        JSONdata = json.dumps({"query": "friends", "author": "555", "authors": self.author2.id})

        # Send a POST request with inconsistent author ID
        response = c.post('/api/friends/%s' % self.author1.id, data=JSONdata, content_type='application/json; charset=utf')

        # Expects a 400 Bad Request
        self.assertEquals(response.status_code, 400, "Response not 400")

    def testFriendQueryPostFailSyntaxList(self):
        """ Test a failed friend query with a JSON value not being a list """

        # JSON with a non-list for authors
        JSONdata = json.dumps({"query": "friends", "author": self.author1.id, "authors": self.author2.id})

        # Send a POST request with invalid JSON
        response = c.post('/api/friends/%s' % self.author1.id, data=JSONdata, content_type='application/json; charset=utf')

        # Expects a 400 Bad Request
        self.assertEquals(response.status_code, 400, "Response not 400")

    def testFriendRequestSuccess(self):
        """ Test sending a successful friend request """
        authorID1 = str(self.author1.id)
        authorID2 = str(self.author2.id)

        # The valid JSON data to be POSTed
        JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID1, "host": "http://127.0.0.1:8000/", "displayname": "Author1"},
                               "friend": {"id": authorID2, "host": "http://127.0.0.1:8000/", "displayname": "Author2",
                                          "url": "http://127.0.0.1:8000/author/"+authorID2}})

        # POST the friend request
        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        # Expect a 200 Ok
        self.assertEquals(response.status_code, 200, "Response not 200")

        # Author1 should now be following Author2
        self.assertTrue(self.author2 in self.author1.follows.all())
        self.assertTrue(len(self.author1.follows.all()) == 1)

    def testFriendRequestSuccessRepeated(self):
        """ Test sending a repeated friend request """
        authorID1 = str(self.author1.id)
        authorID2 = str(self.author2.id)

        # Author1 already has sent a friend request
        self.author1.follows.add(self.author2)

        # The valid JSON data to be POSTed
        JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID1, "host": "http://127.0.0.1:8000/", "displayname": "Author1"},
                               "friend": {"id": authorID2, "host": "http://127.0.0.1:8000/", "displayname": "Author2",
                                          "url": "http://127.0.0.1:8000/author/"+authorID2}})

        # POST the friend request
        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        # Expect a 200 Ok
        self.assertEquals(response.status_code, 200, "Response not 200")

        # Author1 should still be following Author2
        self.assertTrue(self.author2 in self.author1.follows.all())
        self.assertTrue(len(self.author1.follows.all()) == 1)

    def testFriendRequestFailSyntaxKey(self):
        """ Test sending a failed friend request missing author key """
        authorID1 = str(self.author1.id)
        authorID2 = str(self.author2.id)

        # The JSON data missing 'author' key
        JSONdata = json.dumps({"query": "friendrequest", "person": {"id": authorID1, "host": "http://127.0.0.1:8000/", "displayname": "Author1"},
                               "friend": {"id": authorID2, "host": "http://127.0.0.1:8000/", "displayname": "Author2",
                                          "url": "http://127.0.0.1:8000/author/"+authorID2}})

        # POST the friend request
        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        # Expect a 400 Bad Request
        self.assertEquals(response.status_code, 400, "Response not 400")

    def testFriendRequestFailSyntaxObject(self):
        """ Test sending a failed friend request with author value not being an object """
        authorID1 = str(self.author1.id)
        authorID2 = str(self.author2.id)

        # The JSON data with 'author' value not an object
        JSONdata = json.dumps({"query": "friendrequest", "author": authorID1,
                               "friend": {"id": authorID2, "host": "http://127.0.0.1:8000/", "displayname": "Author2",
                                          "url": "http://127.0.0.1:8000/author/"+authorID2}})

        # POST the friend request
        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        # Expect a 400 Bad Request
        self.assertEquals(response.status_code, 400, "Response not 400")

    def testFriendRequestFailSyntaxMissingID(self):
        """ Test sending a failed friend request with missing author ID """
        authorID2 = str(self.author2.id)

        # The JSON data with missing author ID
        JSONdata = json.dumps({"query": "friendrequest", "author": {"host": "http://127.0.0.1:8000/", "displayname": "Author1"},
                               "friend": {"id": authorID2, "host": "http://127.0.0.1:8000/", "displayname": "Author2",
                                          "url": "http://127.0.0.1:8000/author/"+authorID2}})

        # POST the friend request
        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        # Expect a 400 Bad Request
        self.assertEquals(response.status_code, 400, "Response not 400")
