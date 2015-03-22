from Hindlebook.models import User, Post
from api.serializers import PostSerializer, AuthorSerializer, ForeignAuthorSerializer
from model_mommy import mommy
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from django.forms.models import model_to_dict
import json


class PostApiTests(APITestCase):
    """
    Test some of the GET/POST API
    """

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

        # Create Authors
        self.author1 = mommy.make(User)
        self.author2 = mommy.make(User)
        self.author3 = mommy.make(User)

        # Create Private Posts
        self.post1_by_a1 = mommy.make(Post, author=self.author1)
        self.post2_by_a1 = mommy.make(Post, author=self.author1)
        self.post1_by_a2 = mommy.make(Post, author=self.author2)
        self.post1_by_a3 = mommy.make(Post, author=self.author3)

        # Create Private Posts
        self.private1_by_a1 = mommy.make(Post, author=self.author1, visibility='PRIVATE')
        self.private2_by_a1 = mommy.make(Post, author=self.author1, visibility='PRIVATE')
        self.private1_by_a2 = mommy.make(Post, author=self.author2, visibility='PRIVATE')

    def testGETPublicPosts(self):
        """
        GET all public posts
        api method: service/api/posts
        """
        # Make request
        response = self.client.get('/api/posts')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Response not 200")
        self.assertTrue('posts' in response.data, "No 'posts' in response")
        self.assertEquals(len(response.data['posts']), 4,
                          "Should return 4 posts, not " + str(len(response.data['posts'])))

    def testGETPost(self):
        """
        GET a post by given GUID
        api method: service/api/post/{guid}
        """
        # Make request
        url = "/api/post/%s" % self.post1_by_a1.guid
        response = self.client.get(url)

        serializer = PostSerializer(self.post1_by_a1)

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Response not 200")

        # Assert content
        self.assertTrue('posts' in response.data, "No 'posts' in response")
        self.assertTrue(len(response.data['posts']) == 1, "Should return exactly one post")
        self.assertEqual(response.data['posts'][0], serializer.data, "Didn't get correct post information")

    def testPUTUpdatePost(self):
        """
        PUT to update an existing post by GUID
        api method: service/api/post/{guid}
        """
        # Build updated post
        self.post1_by_a1.content = 'This is updated content!'
        serializer = PostSerializer(self.post1_by_a1)

        # Make request
        url = "/api/post/%s" % self.post1_by_a1.guid
        response = self.client.put(url, serializer.data, format='json')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Response not 200")

        # Assert content
        self.assertTrue('posts' in response.data, "No 'posts' in response")
        self.assertTrue(len(response.data['posts']) == 1, "Should return exactly one post")
        self.assertEqual(response.data['posts'][0]['content'],
                         "This is updated content!", "Didn't return correct content")
        self.assertEqual(Post.objects.get(guid=self.post1_by_a1.guid).content,
                         "This is updated content!", "Post didn't get updated")

    def testPUTNewPost(self):
        """
        PUT to insert a new post
        api method: service/api/post/{guid}
        """
        # Build New Post
        guid = "52dfe332-0d07-4adc-89f8-08d6c574e2b8"
        self.post1_by_a1.guid = guid
        serializer = PostSerializer(self.post1_by_a1)

        # Assert New Post is non-existant
        self.assertEquals(Post.objects.filter(guid=self.post1_by_a1.guid).count(), 0, "Post already exists!")

        # Make Request
        url = "/api/post/%s" % guid
        response = self.client.put(url, serializer.data, format='json')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Response not 201")

        # Assert content
        self.assertTrue('posts' in response.data, "No 'posts' in response")
        self.assertTrue(len(response.data['posts']) == 1, "Should return exactly one post")
        # This fails because the time difference in post creation...
        # self.assertEqual(response.data['posts'][0], serializer.data, "Didn't get correct post information")
        data1 = serializer.data
        data1.pop('pubDate')
        data2 = response.data['posts'][0]
        data2.pop('pubDate')
        self.assertEqual(data1, data2, "Didn't get correct post information")
        self.assertEquals(Post.objects.filter(guid=self.post1_by_a1.guid).count(), 1, "Post was not inserted")

    def testPOSTNewPost(self):
        """
        POST to insert a new post
        api method: service/api/post/{guid}
        """
        # Build New Post
        guid = "52dfe332-0d07-4adc-89f8-08d6c574e2b8"
        self.post1_by_a1.guid = guid
        serializer = PostSerializer(self.post1_by_a1)

        # Assert New Post is non-existant
        self.assertEquals(Post.objects.filter(guid=self.post1_by_a1.guid).count(), 0, "Post already exists!")

        # Make Request
        url = "/api/post/%s" % guid
        response = self.client.post(url, serializer.data, format='json')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Response not 201")

        # Assert content
        self.assertTrue('posts' in response.data, "No 'posts' in response")
        self.assertTrue(len(response.data['posts']) == 1, "Should return exactly one post")
        # This fails because the time difference in post creation...
        # self.assertEqual(response.data['posts'][0], serializer.data, "Didn't get correct post information")
        data1 = serializer.data
        data1.pop('pubDate')
        data2 = response.data['posts'][0]
        data2.pop('pubDate')
        self.assertEqual(data1, data2, "Didn't get correct post information")
        self.assertEquals(Post.objects.filter(guid=self.post1_by_a1.guid).count(), 1, "Post was not inserted")

    def testPOSTExistingPost(self):
        """
        POST to insert an existing post (invalid)
        api method: service/api/post/{guid}
        """
        # Build New Post
        serializer = PostSerializer(self.post1_by_a1)

        self.assertEquals(Post.objects.filter(guid=self.post1_by_a1.guid).count(), 1, "Post doesn't exist!")

        # Make Request
        url = "/api/post/%s" % self.post1_by_a1.guid
        response = self.client.post(url, serializer.data, format='json')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Response not 400")

        # print(response.data)
        self.assertEqual(response.data['error'][0], "Post already exists.", "Didn't get correct post information")

    def testGETAuthorPosts(self):
        """
        Test GET posts from given author (visible wrt to the currently authenticated user)
        api method: service/api/author/{uuid}/posts
        """

        url = "/api/author/%s/posts" % self.author1.uuid
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Response not 200")

        # self.assertTrue('posts' in response.data, "No 'posts' in response")
        # self.assertEquals(len(response.data['posts']), 2, "Should return exactly two posts")

        # url = server + "/api/author/%s/posts" % self.author2.uuid
        # response = self.client.get(url)
        # serializer = PostSerializer(different_post)
        # self.assertEqual(response.status_code, status.HTTP_200_OK, "Response not 200")
        # self.assertTrue('posts' in response.data, "No 'posts' in response")
        # self.assertEquals(len(response.data['posts']), 1, "Should return exactly one post")
        # self.assertEquals(response.data['posts'][0], serializer.data, "Didn't get correct post information")

    def testGETVisiblePosts(self):
        """
        Test GET visible posts (visible wrt to the currently authenticated user)
        api method: service/api/author/posts
        """

        url = "/api/author/posts"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Response not 200")

        # self.assertTrue('posts' in response.data, "No 'posts' in response")
        # self.assertEquals(len(response.data['posts']), 2, "Should return exactly two posts")

        # url = server + "/api/author/%s/posts" % self.author2.uuid
        # response = self.client.get(url)
        # serializer = PostSerializer(different_post)
        # self.assertEqual(response.status_code, status.HTTP_200_OK, "Response not 200")
        # self.assertTrue('posts' in response.data, "No 'posts' in response")
        # self.assertEquals(len(response.data['posts']), 1, "Should return exactly one post")
        # self.assertEquals(response.data['posts'][0], serializer.data, "Didn't get correct post information")
