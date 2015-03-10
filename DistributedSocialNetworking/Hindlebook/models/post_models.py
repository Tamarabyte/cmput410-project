from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

import uuid as uuid_import
from Hindlebook.models import ForeignUser
from Hindlebook.models import UuidValidator

class Category(models.Model):
    tag = models.CharField(max_length=25, null=False, blank=False)

    class Meta():
        verbose_name = "Tags"
        verbose_name_plural = "Tags"

class Post(models.Model):
    """Model for representing a Post made by an Author"""

    guid = models.CharField(max_length=40, blank=True, default=uuid_import.uuid4, primary_key=True, validators=[UuidValidator()])
    source = models.CharField(max_length=100, blank=True, default='Unknown source')
    origin = models.CharField(max_length=100, blank=True, default='Unknown origin')

    title = models.CharField(max_length=40, blank=True, default='No title')
    description = models.CharField(max_length=40, blank=True, default='No description')
    categories = models.ManyToManyField(Category, blank=True, related_name='tagged_posts')
    content = models.TextField(blank=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
    pubDate = models.DateTimeField('date published', auto_now_add=True, db_index=True)

    content_type_choices = (("text/plain", "text/plain"), ("text/x-markdown", "text/x-markdown"), ("text/html", "text/html"))
    content_type = models.CharField(max_length=15, blank=True, choices=content_type_choices, default="text/html")

    visibility_choices = (("PUBLIC", "PUBLIC"), ("FOAF", "FOAF"), ("FRIENDS", "FRIENDS"), ("PRIVATE", "PRIVATE"), ("SERVERONLY", "SERVERONLY"))
    visibility = models.CharField(default="PUBLIC", max_length=10, blank=False, choices=visibility_choices, db_index=True)

    def __str__(self):
        return str(self.content)

    # Get the comments for this Post
    def getComments(self):
        return self.comments.all()


class Comment(models.Model):
    """Model for representing a Comment on a Post made by an Author"""

    guid = models.CharField(max_length=40, blank=True, default=uuid_import.uuid4, primary_key=True, validators=[UuidValidator()])
    post = models.ForeignKey(Post, related_name="comments")

    # only author or foreign author should be set
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="comments")
    foreign_author = models.ForeignKey(ForeignUser, null=True, blank=True, related_name="comments")

    comment = models.CharField(max_length=2048)
    pubDate = models.DateTimeField('date published', auto_now_add=True, db_index=True)

    def __str__(self):
        return str(self.guid)

    def getAuthor(self):
        if self.author:
            return self.author
        return self.foreign_author

    def save(self, *args, **kwargs):
        if not self.author and not self.foreign_author:
            raise ValidationError("Requires an author.")

        if self.author and self.foreign_author:
            raise ValidationError("Can't have both an author and a foreign author.")

        return super(Comment, self).save(*args, **kwargs)


class Image(models.Model):
    """Model for representing an Image attached to Posts"""
    attached_to = models.ForeignKey(Post, null=False)
    image = models.ImageField(null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image

