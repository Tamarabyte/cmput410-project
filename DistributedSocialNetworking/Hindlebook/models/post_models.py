from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

import uuid as uuid_import
from Hindlebook.models import ForeignUser

class Category(models.Model):
    tag = models.CharField(max_length=25, null=False, blank=False)

    class Meta():
        verbose_name = "Tags"
        verbose_name_plural = "Tags"

class Post(models.Model):
    """Model for representing a Post made by an Author"""

    uuid = models.CharField(max_length=40, blank=True, default=uuid_import.uuid4, primary_key=True)
    source = models.CharField(max_length=100, blank=True, default='Unknown source')
    origin = models.CharField(max_length=100, blank=True, default='Unknown origin')

    title = models.CharField(max_length=40, blank=True, default='No title')
    description = models.CharField(max_length=40, blank=True, default='No description')
    categories = models.ManyToManyField(Category, blank=True, related_name='tagged_posts')
    text = models.TextField(blank=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
    pub_date = models.DateTimeField('date published', auto_now_add=True, db_index=True)

    content_type_choices = ((0,"text/plain"), (1,"text/x-markdown"), (2,"text/html"))
    content_type = models.IntegerField(max_length=1, blank=True, choices=content_type_choices, default=0)

    privacy_choices = ((0, "PUBLIC"), (1, "FOAF"), (2, "FRIENDS"), (3, "PRIVATE"), (4, "SERVERONLY"))
    privacy = models.IntegerField(default=0, max_length=1, choices=privacy_choices, db_index=True)

    def __str__(self):
        return str(self.text)

    # Get the comments for this Post
    def getComments(self):
        return self.comments.all()


class Comment(models.Model):
    """Model for representing a Comment on a Post made by an Author"""

    uuid = models.CharField(max_length=40, blank=True, default=uuid_import.uuid4, primary_key=True)
    post = models.ForeignKey(Post, related_name="comments")

    # only author or foreign author should be set
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="comments")
    foreign_author = models.ForeignKey(ForeignUser, null=True, blank=True, related_name="comments")

    text = models.CharField(max_length=2048)
    pub_date = models.DateTimeField('date published', auto_now_add=True, db_index=True)

    def __str__(self):
        return str(self.uuid)

    def getAuthor(self):
        if self.author:
            return self.author
        return self.foreign_author

    def clean(self):
        if not self.author and not self.foreign_author:
            raise ValidationError("Requires an author.")

        if self.author and self.foreign_author:
            raise ValidationError("Can't have both an author and a foreign author.")


class Image(models.Model):
    """Model for representing an Image attached to Posts"""
    attached_to = models.ForeignKey(Post, null=False)
    image = models.ImageField(null=False)
    date_added = models.DateTimeField(auto_now_add=True)

