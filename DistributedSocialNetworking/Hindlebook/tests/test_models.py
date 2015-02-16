from django.test import TestCase
from Hindlebook.models import Author, Post
from model_mommy import mommy


class AuthorTestCases(TestCase):
    """ Tests related to Author model """

    def setUp(self):
        self.author1 = mommy.make(Author)
        self.author2 = mommy.make(Author)

    # Test Author Creation
    def test_author_create(self):
        self.assertTrue(isinstance(self.author1, Author))
        self.assertEquals(self.author1.user.username, str(self.author1))
        self.assertQuerysetEqual(self.author1.follows.all(), [])
        self.assertQuerysetEqual(self.author1.followed_by.all(), [])
        self.assertQuerysetEqual(self.author1.getFriends(), [])
        self.assertQuerysetEqual(self.author1.getFriends(), self.author2.getFriends())

    # Test following
    def test_following(self):
        # Author1 follows Author2
        self.author1.follows.add(self.author2)
        self.assertQuerysetEqual(self.author1.follows.all(), ["<Author: %s>" % self.author2.user.username])
        self.assertQuerysetEqual(self.author2.followed_by.all(), ["<Author: %s>" % self.author1.user.username])

        # Assert asymmetrical following
        self.assertQuerysetEqual(self.author2.follows.all(), [])
        self.assertQuerysetEqual(self.author1.followed_by.all(), [])

    # Test Friends
    def test_friends(self):
        # Test one way friendship
        self.author2.follows.add(self.author1)
        self.assertQuerysetEqual(self.author1.getFriends(), [])
        self.assertQuerysetEqual(self.author1.getFriends(), self.author2.getFriends())

        # Test reflexive friendship
        self.author1.follows.add(self.author2)
        self.assertQuerysetEqual(self.author1.getFriends(), ["<Author: %s>" % self.author2.user.username])
        self.assertQuerysetEqual(self.author2.getFriends(), ["<Author: %s>" % self.author1.user.username])

    # Test Friend Requests
    def test_friend_requests(self):
        self.assertQuerysetEqual(self.author1.getFriendRequests(), [])
        self.author2.follows.add(self.author1)
        self.assertQuerysetEqual(self.author1.getFriendRequests(), ["<Author: %s>" % self.author2.user.username])


class PostTestCases(TestCase):
    """Tests Related to Post model"""
    def setUp(self):
        self.author1 = mommy.make(Author)
        self.author2 = mommy.make(Author)
        self.post1_by_a1 = mommy.make(Post, author=self.author1)
        self.post2_by_a1 = mommy.make(Post, author=self.author1)
        self.post1_by_a2 = mommy.make(Post, author=self.author2)

    # Test Post creation
    def test_post_create(self):
        # Authors can have multiple posts
        self.assertEquals(self.post1_by_a1.author.user.username, self.author1.user.username)
        self.assertEquals(self.post2_by_a1.author.user.username, self.author1.user.username)

    # Test Post privacy
    def test_post_privacy(self):
        pass

    # Test fetching own Posts
    def test_get_own_posts(self):
        pass

    # Test fetching others Posts
    def test_get_other_posts(self):
        pass


class CommentTestCases(TestCase):
    """Tests Related to Comment model"""
    def setUp(self):
        self.author1 = mommy.make(Author)
        self.author2 = mommy.make(Author)
        self.post_by_a1 = mommy.make(Post, author=self.author1)
        self.otherpost_by_a1 = mommy.make(Post, author=self.author1)
        self.post_by_a2 = mommy.make(Post, author=self.author2)

    # Test Comment creation
    def test_comment_creation(self):
        pass


class ImageTestCases(TestCase):
    """Tests Related to Image model"""
    def setUp(self):
        pass

    # Test Image creation
    def test_comment_creation(self):
        pass