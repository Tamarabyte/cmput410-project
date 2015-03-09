from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid as uuid_import
from Hindlebook.models import Node, Server

class User(AbstractUser):
    """Model for represting a User"""

    uuid = models.CharField(max_length=40, blank=True, default=uuid_import.uuid4, db_index=True)

    github_id = models.CharField(max_length=30, blank=True, default='')
    avatar = models.ImageField(null=True, blank=True)
    about = models.CharField(max_length=250, blank=True, default="")

    follows = models.ManyToManyField('self', blank=True, related_name='followed_by', symmetrical=False, db_index=True)
    follows_foreign = models.ManyToManyField('self', blank=True, related_name='followed_by', db_index=True)
    node = models.ForeignKey(Server, related_name="users", blank=True, default=1)

    def __str__(self):
        return self.username

    # Two way following implies "real" friendship
    def getFriends(self):
        return self.follows.all() & self.followed_by.all()

    # Those which are following me but I am not following back
    def getFriendRequests(self):
        A = self.followed_by.all()
        B = self.follows.all()
        return A.exclude(pk__in=B)
    
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

    uuid = models.CharField(max_length=40, blank=True, default=uuid_import.uuid4, primary_key=True)
    node = models.ForeignKey(Node, related_name="users")
    username = models.CharField('username', max_length=30, blank=False)

