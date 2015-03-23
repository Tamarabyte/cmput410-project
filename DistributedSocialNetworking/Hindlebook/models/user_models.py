from django.db import models
from django.contrib.auth.models import User
from itertools import chain
import uuid as uuid_import
from Hindlebook.models import Node, UuidValidator

class Author(models.Model):
    """Model for represting a Authors"""

    user = models.OneToOneField(User, related_name="author", blank=True, null=True)
    about = models.CharField(max_length=250, blank=True, default="")
    uuid = models.CharField(max_length=40, blank=True, default=uuid_import.uuid4, validators=[UuidValidator()], primary_key=True)
    username = models.CharField('username', max_length=30, blank=False)
    
    friends = models.ManyToManyField('self', blank=True, related_name='friends_of', symmetrical=False, db_index=True)
    follows = models.ManyToManyField('self', blank=True, related_name='followed_by', symmetrical=False, db_index=True)
    github_id = models.CharField(max_length=30, blank=True, default='')
    avatar = models.ImageField(null=False, blank=True, default="default_avatar.jpg")
    node = models.ForeignKey(Node, related_name="authors")
    date_added = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return self.username

