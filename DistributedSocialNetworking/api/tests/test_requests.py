# from django.test import TestCase
# from model_mommy import mommy
# from Hindlebook.models import Author, Post, Node
from api.requests import PublicPostsRequestFactory
# import requests


# class PublicPostRequestTestCases(TestCase):
#     """
#     Tests related to Public Post Requests
#     """
#     def setUp(self):
#         # Create Node
#         self.node1 = mommy.make(Node, host='test', password='test')

#         # Create Authors
#         self.author1 = mommy.make(Author)
#         self.author2 = mommy.make(Author)
#         self.author3 = mommy.make(Author)

#         # Create Public Posts
#         self.post1_by_a1 = mommy.make(Post, author=self.author1)
#         self.post2_by_a1 = mommy.make(Post, author=self.author1)
#         self.post1_by_a2 = mommy.make(Post, author=self.author2)
#         self.post1_by_a3 = mommy.make(Post, author=self.author3)

#         # Create Private Posts
#         self.private1_by_a1 = mommy.make(Post, author=self.author1, visibility='PRIVATE')
#         self.private2_by_a1 = mommy.make(Post, author=self.author1, visibility='PRIVATE')
#         self.private1_by_a2 = mommy.make(Post, author=self.author2, visibility='PRIVATE')

#     def testRequest(self):
#         """
#         GET all public posts
#         api method: service/api/posts
#         """
#         # Make request
#         host = "testserver"
#         response = PublicPostsRequestFactory.create(host).send()

#         data = response.json()

#         # Assert response
#         self.assertEqual(response.status_code, requests.codes.ok, "Response not 200")
#         self.assertTrue('posts' in data, "No 'posts' in response")
#         self.assertEquals(len(data['posts']), 4,
#                           "Should return 4 posts, not " + str(len(data['posts'])))
