from django.db import models
from django.contrib.auth.models import AbstractUser

from itertools import chain

import uuid as uuid_import

from Hindlebook.models import Node, Server, UuidValidator


class User(AbstractUser):
    """Model for represting a User"""

    uuid = models.CharField(max_length=40, blank=True, default=uuid_import.uuid4, db_index=True, validators=[UuidValidator()])

    github_id = models.CharField(max_length=30, blank=True, default='')
    avatar = models.ImageField(null=False, blank=True, default="default_avatar.jpg")
    about = models.CharField(max_length=250, blank=True, default="")

    follows = models.ManyToManyField('self', blank=True, related_name='followed_by', symmetrical=False, db_index=True)
    follows_foreign = models.ManyToManyField('self', blank=True, related_name='followed_by', db_index=True)
    
    friends = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='friends_of', db_index=True)
    friends_foreign = models.ManyToManyField('self', blank=True, related_name='friends', db_index=True)
    
    node = models.ForeignKey(Server, related_name="users", blank=True, default=1)

    def __str__(self):
        return self.username

    # Two way friends implies "real" friendship
    def getFriends(self):
        return self.friends.all() & self.friends_of.all()

    def getFriendsOfFriends(self):
        friends = self.getFriends()
        friends_ext = friends
        for f in friends:
            friends_ext = chain(friends_ext, f.getFriends())
        return friends_ext

    # Friend requests that I haven't accepted
    def getFriendRequests(self):
        A = self.friends_of.all()
        B = self.friends.all()
        return A.exclude(pk__in=B)

    # Those which I friend but do not friend back
    def getUnacceptedFriends(self):
        A = self.friends_of.all()
        B = self.friends.all()
        return B.exclude(pk__in=A)

    # Get the count of friend requests
    def getFriendRequestCount(self):
        return len(self.getFriendRequests())

    # Get Authors own posts
    def getAuthoredPosts(self):
        return self.posts.all()

    # Get Authors own Comments
    def getAuthoredComments(self):
        return self.comments.all()


class ForeignUser(models.Model):
    """Model for represting a Foreign Users"""

    uuid = models.CharField(max_length=40, blank=True, default=uuid_import.uuid4, validators=[UuidValidator()])
    node = models.ForeignKey(Node, related_name="users")
    username = models.CharField('username', max_length=30, blank=False)

    # generics = GenericRelation(GenericUser)

    def __str__(self):
        return self.username

