from django.test import TestCase
from Hindlebook.models import Author
from model_mommy import mommy


class AuthorTestCases(TestCase):

    def test_author_create(self):
        a = mommy.make('Hindlebook.Author')
        self.assertTrue(isinstance(a, Author))
        self.assertEquals(a.user.username, str(a))
        self.assertQuerysetEqual(a.follows.all(), [])
        self.assertQuerysetEqual(a.followed_by.all(), [])

    def test_followers(self):
        a = mommy.make('Hindlebook.Author')
        b = mommy.make('Hindlebook.Author')

        a.follows.add(b)
        self.assertQuerysetEqual(a.follows.all(), ["<Author: %s>" % b.user.username])
        self.assertQuerysetEqual(b.followed_by.all(), ["<Author: %s>" % a.user.username])
        self.assertQuerysetEqual(b.follows.all(), [])
        self.assertQuerysetEqual(a.followed_by.all(), [])

    def test_friends(self):
        a = mommy.make('Hindlebook.Author')
        b = mommy.make('Hindlebook.Author')

        self.assertQuerysetEqual(a.getFriends(), [])
        self.assertQuerysetEqual(a.getFriends(), b.getFriends())

        a.follows.add(b)
        self.assertQuerysetEqual(a.getFriends(), [])
        self.assertQuerysetEqual(b.getFriends(), [])

        b.follows.add(a)
        self.assertQuerysetEqual(a.getFriends(), ["<Author: %s>" % b.user.username])
        self.assertQuerysetEqual(b.getFriends(), ["<Author: %s>" % a.user.username])

    def test_friend_requests(self):
        a = mommy.make('Hindlebook.Author')
        b = mommy.make('Hindlebook.Author')

        self.assertQuerysetEqual(a.getFriendRequests(), [])
        b.follows.add(a)
        self.assertQuerysetEqual(a.getFriendRequests(), ["<Author: %s>" % b.user.username])

