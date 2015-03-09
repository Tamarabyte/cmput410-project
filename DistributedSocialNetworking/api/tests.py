from django.test import TestCase, Client
from Hindlebook.models import User, Post
from Hindlebook.serializers import PostSerializer
from model_mommy import mommy
import json

c = Client()


class APITests(TestCase):
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

    def testGETPost(self):
        """ Test GET an author post by given post ID """

        serializer = PostSerializer(self.post1)
        originalPost = serializer.data

        # Send a GET request with the post id
        response = c.get('/api/post/%s' % self.post1.uuid)

        # Expects a 200 Ok with a JSON response
        self.assertEquals(response.status_code, 200, "Response not 200")

        # Decode the JSON response
        decoded = json.loads(response.content.decode('utf-8'))

        # Serialize the response
        serializer = PostSerializer(data=decoded)

        self.assertTrue(serializer.is_valid(), "Returned invalid JSON")
        responsePost = serializer.data

        self.assertEquals(originalPost, responsePost, "Returned incorrect information")

    def testPOSTPost(self):
        """ Test POST an author post by given post ID """

        serializer = PostSerializer(self.post1)
        originalPost = serializer.data

        # Send a POST request with the post id
        response = c.post('/api/post/%s' % self.post1.uuid)

        # Expects a 200 Ok with a JSON response
        self.assertEquals(response.status_code, 200, "Response not 200")

        # Decode the JSON response
        decoded = json.loads(response.content.decode('utf-8'))

        # Serialize the response
        serializer = PostSerializer(data=decoded)

        self.assertTrue(serializer.is_valid(), "Returned invalid JSON")
        responsePost = serializer.data

        self.assertEquals(originalPost, responsePost, "Returned incorrect information")

    def testPUTPost(self):
        """ Test PUT an author post by given post ID """

        # Send a GET request with post id
        response = c.get('/api/post/%s' % self.post1.uuid)

        # Decode the JSON response
        decoded = json.loads(response.content.decode('utf-8'))
        serializer = PostSerializer(data=decoded)

        self.assertTrue(serializer.is_valid(), "Returned invalid JSON")
        originalPost = serializer.data

        serializer = PostSerializer(self.post2)
        newPost = serializer.data

        JSONdata = json.dumps(newPost)

        # Send a PUT request to update the existing post
        response = c.put('/api/post/%s' % self.post1.uuid, data=JSONdata, content_type='application/json; charset=utf')

        # Decode the JSON response
        decoded = json.loads(response.content.decode('utf-8'))
        serializer = PostSerializer(data=decoded)

        self.assertTrue(serializer.is_valid(), "Returned invalid JSON")

        self.assertEquals(response.status_code, 200, "Response not 200")

        responsePost = serializer.data

        self.assertNotEquals(responsePost, originalPost, "Post not updated")
        self.assertEquals(responsePost, newPost, "Post not updated correctly")

    def testFriend2FriendGetQuerySuccess(self):
        """ Test a successful friend2friend query """

        self.author1.follows.add(self.author2)
        self.author2.follows.add(self.author1)

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

        self.author1.follows.add(self.author2)
        self.author2.follows.add(self.author1)

        JSONdata = json.dumps({"query": "friends", "author": id1, "authors": [5, 6, 7, id2, 3]})

        response = c.post('/api/friends/%s' % id1, data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        decoded = json.loads(response.content.decode('utf-8'))

        self.assertEquals(decoded['query'], "friends", "JSON response needs \"query\":\"friends\"")
        self.assertEquals(decoded['author'], id1, "Author has incorrect ID")
        self.assertEquals(len(decoded['friends']), 1, "Author should have exactly one friend")
        self.assertEquals(decoded['friends'][0], id2, "Authors are not friends but they should be")

    def testFriendRequestSuccess(self):
        """ Test sending a successful friend request """

        authorID1 = str(self.author1.uuid)
        authorID2 = str(self.author2.uuid)

        JSONdata = json.dumps({"query": "friendrequest", "author": {"id": authorID1, "host": "http://127.0.0.1:8000/", "displayname": "Author1"},
                               "friend": {"id": authorID2, "host": "http://127.0.0.1:8000/", "displayname": "Author2",
                                          "url": "http://127.0.0.1:8000/author/"+authorID2}})

        response = c.post('/api/friendrequest', data=JSONdata, content_type='application/json; charset=utf')

        self.assertEquals(response.status_code, 200, "Response not 200")

        self.assertTrue(self.author2 in self.author1.follows.all())
        self.assertTrue(len(self.author1.follows.all()) == 1)

    def testGETAuthorPosts(self):
        """ Test GET posts from given author """

        post1 = mommy.make(Post, author=self.author1)
        post2 = mommy.make(Post, author=self.author1)
        different_post = mommy.make(Post, author=self.author2)

        response = c.get('/api/author/%s/posts' % self.author1.uuid)

        self.assertEquals(response.status_code, 200, "Response not 200")

        jsonString = json.loads(response.content.decode('utf-8'))
        jsonObject = json.loads(jsonString)

        self.assertEquals(len(jsonObject), 2, "Author should have 2 posts")

        for post in jsonObject:
            serializer = PostSerializer(data=post)
            self.assertTrue(serializer.is_valid(), "Returned invalid JSON")
            postData = serializer.data

    def testGETAuthorPostText(self):
        """ Test GET post text from given author """

        post1 = mommy.make(Post, author=self.author1)
        different_post = mommy.make(Post, author=self.author2)

        response = c.get('/api/author/%s/posts' % self.author1.uuid)

        self.assertEquals(response.status_code, 200, "Response not 200")

        jsonString = json.loads(response.content.decode('utf-8'))
        jsonObject = json.loads(jsonString)

        self.assertEquals(len(jsonObject), 1, "Author should have 1 post")

        for post in jsonObject:
            serializer = PostSerializer(data=post)
            self.assertTrue(serializer.is_valid(), "Returned invalid JSON")
            postData = serializer.data
            self.assertEquals(postData['text'], post1.text, "Post has wrong text")

    def testGETPublicPosts(self):
        """ Test GET all public posts """

        # Posts are public by default
        publicPost = mommy.make(Post)

        # Make a private post
        privatePost = mommy.make(Post, privacy=0)

        response = c.get('/api/posts')

        self.assertEquals(response.status_code, 200, "Response not 200")

        jsonString = json.loads(response.content.decode('utf-8'))
        jsonObject = json.loads(jsonString)

        self.assertEquals(len(jsonObject), 3, "Should be 2 public post")

        for post in jsonObject:
            serializer = PostSerializer(data=post)
            self.assertTrue(serializer.is_valid(), "Returned invalid JSON")
            postData = serializer.data
