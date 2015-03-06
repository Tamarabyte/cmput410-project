from django.db import models
from django.conf import settings

class Post(models.Model):
    """Model for representing a Post made by an Author"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return str(self.id)

    # Get the comments for this Post
    def getComments(self):
        return self.comments.all()


class Comment(models.Model):
    """Model for representing a Comment on a Post made by an Author"""
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments")
    text = models.CharField(max_length=2048)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Image(models.Model):
    """Model for representing an Image attached to Posts"""
    attached_to = models.ManyToManyField(Post, null=True)
    image = models.ImageField(null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    