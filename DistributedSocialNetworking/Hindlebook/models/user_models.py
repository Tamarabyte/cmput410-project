from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    """Model for represting a User"""
    avatar = models.ImageField(null=True, blank=True, width_field=100, height_field=100)
    github_id = models.CharField(max_length=30, null=False, blank=True, default='')
    about = models.CharField(max_length=250, null=False, blank=True, default="This user hasn't filled out their profile yet!")
    follows = models.ManyToManyField('self', blank=True, related_name='followed_by', symmetrical=False)
    uuid = models.CharField(max_length=40, blank=True, default=uuid.uuid4)
    host = models.CharField(max_length=100, blank=True, default='')
    
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

    # Get Authors own posts
    def getAuthoredPosts(self):
        return self.posts.all()

    # Get Authors own Comments
    def getAuthoredComments(self):
        return self.comments.all()

