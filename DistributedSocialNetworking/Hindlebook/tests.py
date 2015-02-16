from django.test import TestCase
from models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="test1@google.com", password="123shoe")
