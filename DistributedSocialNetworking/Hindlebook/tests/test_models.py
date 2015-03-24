from django.test import TestCase

from itertools import chain

from Hindlebook.models import Author, Post, Comment
from model_mommy import mommy


class AuthorTestCases(TestCase):
    """ Tests related to Author model """

    def setUp(self):
        self.author1 = mommy.make(Author)
        self.author2 = mommy.make(Author)

    # Test Author Creation
    def test_author_create(self):
        self.assertTrue(isinstance(self.author1, Author))
        self.assertEquals(self.author1.username, str(self.author1))
        self.assertQuerysetEqual(self.author1.follows.all(), [])
        self.assertQuerysetEqual(self.author1.followed_by.all(), [])
        self.assertQuerysetEqual(self.author1.getFriends(), [])
        self.assertQuerysetEqual(self.author1.getFriends(), self.author2.getFriends())

    # Test following
    def test_following(self):
        # Author1 follows Author2
        self.author1.follows.add(self.author2)
        self.assertQuerysetEqual(self.author1.follows.all(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.followed_by.all(), ["<Author: %s>" % self.author1.username])

        # Assert asymmetrical following
        self.assertQuerysetEqual(self.author2.follows.all(), [])
        self.assertQuerysetEqual(self.author1.followed_by.all(), [])

    # Test Friends
    def test_friends(self):
        # Test one way friendship
        self.author2.friends.add(self.author1)
        self.assertQuerysetEqual(self.author1.getFriends(), [])
        self.assertQuerysetEqual(self.author1.getFriends(), self.author2.getFriends())

        # Test reflexive friendship
        self.author1.friends.add(self.author2)
        self.assertQuerysetEqual(self.author1.getFriends(), ["<Author: %s>" % self.author2.username])
        self.assertQuerysetEqual(self.author2.getFriends(), ["<Author: %s>" % self.author1.username])

    # Test Friend Requests
    def test_friend_requests(self):
        self.assertQuerysetEqual(self.author1.getFriendRequests(), [])
        self.author2.friends.add(self.author1)
        self.assertQuerysetEqual(self.author1.getFriendRequests(), ["<Author: %s>" % self.author2.username])


class PostTestCases(TestCase):
    """Tests Related to Post model"""
    def setUp(self):
        self.author1 = mommy.make(Author)
        self.author2 = mommy.make(Author)
        self.post1_by_a1 = mommy.make(Post, author=self.author1, visibility="PUBLIC")
        self.post2_by_a1 = mommy.make(Post, author=self.author1, visibility="PRIVATE")
        self.post1_by_a2 = mommy.make(Post, author=self.author2, visibility="PUBLIC")

    # Test Post creation
    def test_post_create(self):
        # Authors can have multiple posts
        self.assertEquals(self.post1_by_a1.author.username, self.author1.username)
        self.assertEquals(self.post2_by_a1.author.username, self.author1.username)

    # Test Post privacy
    def test_post_privacy(self):
        self.assertQuerysetEqual(Post.objects_ext.get_all_visibile_posts(self.author1), chain(self.post1_by_a1, self.post1_by_a2, self.post2_by_a1))
        self.assertQuerysetEqual(Post.objects_ext.get_all_visibile_posts(self.author2), chain(self.post1_by_a1, self.post2_by_a1))

    # Test fetching own Posts
    def test_getAuthoredPosts(self):
        self.assertQuerysetEqual(self.author2.getAuthoredPosts(),
                                 ["<Post: %s>" % self.post1_by_a2.content])
        self.assertQuerysetEqual(self.author1.getAuthoredPosts().order_by('pubDate'),
                                 ["<Post: %s>" % self.post1_by_a1.content,
                                  "<Post: %s>" % self.post2_by_a1.content])


class CommentTestCases(TestCase):
    """Tests Related to Comment model"""
    def setUp(self):
        self.author1 = mommy.make(Author)
        self.author2 = mommy.make(Author)
        self.post1_by_a1 = mommy.make(Post, author=self.author1)
        self.post2_by_a1 = mommy.make(Post, author=self.author1)
        self.post_by_a2 = mommy.make(Post, author=self.author2)
        self.comment_by_a2_on_post1_by_a1 = mommy.make(Comment,
                                                       author=self.author2,
                                                       post=self.post1_by_a1)

    # Test Comment creation
    def test_comment_creation(self):
        self.assertEquals(self.comment_by_a2_on_post1_by_a1.author.username,
                          self.author2.username)

    # Test fetching Authors Comments
    def test_getAuthoredComments(self):
        self.assertQuerysetEqual(self.author2.getAuthoredComments(),
                                 ["<Comment: %s>" % self.comment_by_a2_on_post1_by_a1.guid])

    # Test fetching Posts Comments
    def test_getPostsComments(self):
        self.assertQuerysetEqual(self.post1_by_a1.getComments(),
                                 ["<Comment: %s>" % self.comment_by_a2_on_post1_by_a1.guid])


class ImageTestCases(TestCase):
    """Tests Related to Image model"""
    def setUp(self):
        pass

    # Test Image creation
    def test_comment_creation(self):
        pass
