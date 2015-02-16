from django.test import TestCase
from Hindlebook.models import User
from model_mommy import mommy


class ModelTestCases(TestCase):

    def test_user_create(self):
        new_user1 = mommy.make('Hindlebook.User')
        new_user2 = mommy.make('Hindlebook.User')
        self.assertTrue(isinstance(new_user1, User))
        self.assertTrue(isinstance(new_user2, User))
        self.assertNotEquals(new_user1.email, new_user2.email)
