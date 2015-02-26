from django.test import TestCase, Client
from Hindlebook.models import Author
from model_mommy import mommy
import json

c = Client()


class APITests(TestCase):
    """ Test some of the GET/POST API """

    def setUp(self):
        self.author1 = mommy.make(Author)
        self.author2 = mommy.make(Author)

    def tearDown(self):
        Author.objects.all().delete()

    def testFriend2FriendGetQuery(self):
        """Check if 2 authors are friends via GET"""

        # Set the 2 authors to be 'real' friends
        self.author1.follows.add(self.author2)
        self.author2.follows.add(self.author1)

        # Send a GET request to check if they are friends
        response = c.get('/friends/%s/%s' % (self.author1.id, self.author2.id))

        # Should receive a 200 Ok with a JSON response
        self.assertNotEquals(response.status_code, 404, "Received a 404")
        self.assertEquals(response.status_code, 200, "Response not 200")

        decoded = json.loads(response.content.decode('utf-8'))

        # Expects a JSON response similar to:
        # https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
        # except hindle's specifies "friends":[id1, id2], and also "friends":"YES", but they shouldn't be the same key name??
        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['authors'][0], str(self.author1.id), "First author has incorrect ID")
        self.assertEquals(decoded['authors'][1], str(self.author2.id), "Second author has incorrect ID")
        self.assertEquals(decoded['friends'], "YES", "Authors are not friends but should be")

    def testFriendQueryPost(self):
        """Check if a given author is friends with any in a POST JSON list"""

        # Set the 2 authors to be 'real' friends
        self.author1.follows.add(self.author2)
        self.author2.follows.add(self.author1)

        # JSON specifying a list of authors to check friendship with author1
        JSONdata = json.dumps({"query": "friends", "author": self.author1.id, "authors": [5, 6, 7, 2, 3]})

        # Send a POST request to check if author1 is friends with anyone in the authors list
        response = c.post('/friends/%s' % self.author1.id, data=JSONdata, content_type='application/json; charset=utf')

        # Should receive a 200 Ok with a JSON response
        self.assertNotEquals(response.status_code, 404, "Received a 404")
        self.assertEquals(response.status_code, 200, "Response not 200")

        decoded = json.loads(response.content.decode('utf-8'))

        # Expects a JSON response with the below values
        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['author'], str(self.author1.id), "Author has incorrect ID")
        self.assertEquals(len(decoded['friends']), 1, "Author should have exactly one friend")
        self.assertEquals(decoded['friends'][0], self.author2.id, "Authors are not friends but they should be")
