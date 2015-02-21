from django.test import TestCase, Client
from Hindlebook.models import Author
from model_mommy import mommy
import json

c = Client()

class APITests(TestCase):

    def setUp(self):
        self.author1 = mommy.make(Author)
        self.author2 = mommy.make(Author)

    def tearDown(self):
        Author.objects.all().delete()

    def testGetFriend2Friend(self):
        """Check friendship"""

        # Set the 2 authors to be 'real' friends
        self.author1.follows.add(self.author2)
        self.author2.follows.add(self.author1)

        # Send a GET request to check if they are friends
        response = c.get('/friends/%s/%s' %(self.author1.id, self.author2.id))

        # Should receive a 200 Ok with a JSON response
        self.assertNotEquals(response.status_code, 404, "Received a 404 response")
        self.assertEquals(response.status_code, 200, "Friendship not retrieved Ok")

        decoded = json.loads(response.content)

        # Note that the format of this JSON response isn't currently the format specified at
        # https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
        # hindle's specifies "friends":[id1, id2], and also "friends":"YES", but they shouldn't be the same key name??
        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['authors'][0], str(self.author1.id), "First author has incorrect ID")
        self.assertEquals(decoded['authors'][1], str(self.author2.id), "Second author has incorrect ID")
        self.assertEquals(decoded['friends'], "YES", "Authors are not friends but should be")
