from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """Model for represting an Author (subclass of User)"""
    user = models.OneToOneField(User)
    github_id = models.CharField(max_length=30, null=True)
    join_date = models.DateField('date joined', auto_now_add=True)
    follows = models.ManyToManyField('self', blank=True, related_name='followed_by', symmetrical=False)
    profile_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    # Two way following implies "real" friendship
    def getFriends(self):
        return self.follows.all() & self.followed_by.all()

    # Those which are following me but I am not following back
    def getFriendRequests(self):
        A = self.followed_by.all()
        B = self.follows.all()
        return A.exclude(pk__in=B)

    # Get my own posts
    def getAuthoredPosts():
        pass


class Post(models.Model):
    """Model for representing a Post made by an Author"""
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    privacy_level = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return str(self.text)


class Comment(models.Model):
    """Model for representing a Comment on a Post made by an Author"""
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    text = models.CharField(max_length=2048)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return str(self.text)


class Image(models.Model):
    """Model for representing an Image attached to Posts"""
    id = models.AutoField(primary_key=True)
    attached_to = models.ManyToManyField(Post, null=True)
