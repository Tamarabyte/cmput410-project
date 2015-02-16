from django.test import TestCase
from Hindlebook.models import User
from model_mommy import mommy


class UserTestCases(TestCase):

    def test_user_create(self):
        a = mommy.make('Hindlebook.User')
        self.assertTrue(isinstance(a, User))
        self.assertEquals(a.email, str(a))
        self.assertQuerysetEqual(a.follows.all(), [])
        self.assertQuerysetEqual(a.followed_by.all(), [])

    def test_followers(self):
        a = mommy.make('Hindlebook.User')
        b = mommy.make('Hindlebook.User')

        a.follows.add(b)
        self.assertQuerysetEqual(a.follows.all(), ["<User: %s>" % b.email])
        self.assertQuerysetEqual(b.followed_by.all(), ["<User: %s>" % a.email])
        self.assertQuerysetEqual(b.follows.all(), [])
        self.assertQuerysetEqual(a.followed_by.all(), [])

    def test_friends(self):
        a = mommy.make('Hindlebook.User')
        b = mommy.make('Hindlebook.User')

        self.assertQuerysetEqual(a.getFriends(), [])
        self.assertQuerysetEqual(a.getFriends(), b.getFriends())

        a.follows.add(b)
        self.assertQuerysetEqual(a.getFriends(), [])
        self.assertQuerysetEqual(b.getFriends(), [])

        b.follows.add(a)
        self.assertQuerysetEqual(a.getFriends(), ["<User: %s>" % b.email])
        self.assertQuerysetEqual(b.getFriends(), ["<User: %s>" % a.email])

    def test_friend_requests(self):
        a = mommy.make('Hindlebook.User')
        b = mommy.make('Hindlebook.User')

        self.assertQuerysetEqual(a.getFriendRequests(), [])
        b.follows.add(a)
        self.assertQuerysetEqual(a.getFriendRequests(), ["<User: %s>" % b.email])

