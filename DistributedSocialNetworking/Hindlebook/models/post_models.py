from Hindlebook.models.user_models import ForeignUser
from Hindlebook.models import UuidValidator

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from itertools import chain
import uuid as uuid_import
import functools
import operator


class Category(models.Model):
    tag = models.CharField(max_length=25, null=False, blank=False, unique=True)

    class Meta():
        verbose_name = "Tags"
        verbose_name_plural = "Tags"


class ExtendedPostManager(models.Manager):

    def get_all_visibile_posts(self, active_user, reversed=True, min_time=None):
        """Gets all the posts visible to the provided user"""
        #  Get list of friends
        friends = active_user.getFriends()
        #  Get list of friends of friends
        friends_ext = active_user.getFriendsOfFriends()

        #  This is a safe way to add values to the filters that could be None
        q_list = [Q()]
        if min_time is not None:
            q_list.append(Q(pubDate__gt=min_time))
        q_reduced = functools.reduce(operator.and_, q_list)

        my_posts = Post.objects.filter(q_reduced, author=active_user)  # My posts
        public_posts = Post.objects.filter(q_reduced, visibility="PUBLIC").exclude(author=active_user)  # Public Posts
        friend_posts = Post.objects.filter(q_reduced, visibility="FRIENDS", author__in=friends).exclude(author=active_user)  # Friend Posts from my frineds
        foff_posts = Post.objects.filter(q_reduced, visibility="FOAF", author__in=friends_ext).exclude(author=active_user)  # FOAF posts from FOAFS

        #  Merge lists
        all_visible_posts = sorted(
            chain(my_posts, public_posts, friend_posts, foff_posts,),
            key=lambda instance: instance.pubDate, reverse=reversed)
        return all_visible_posts

    def get_profile_visibile_posts(self, active_user, page_user):
        """Get all the posts made by page_user that are visible to active_user"""

        #  Is the active user the user they are looking at
        if active_user == page_user:
            return Post.objects.filter(author=page_user).ordered_by(-pubDate)

        #  Get list of friends
        friends = active_user.getFriends()
        #  Get list of friends of friends
        friends_ext = active_user.getFriendsOfFriends()

        #  Get the public posts by the page_user
        public_posts = Post.objects.filter(visibility="PUBLIC", author=page_user)
        friend_posts = {}
        foff_posts = {}
        #  Is the page_user a friend then get their friends only posts
        if page_user in friends:
            friend_posts = Post.objects.filter(visibility="FRIENDS", author=page_user)
        #  Is the page_user a friend of a friend then get their FOAF only posts
        if page_user in friends_ext:
            foff_posts = Post.objects.filter(visibility="FOAF", author=page_user)

        #  Merge into one set sorted by inverse date
        all_visible_posts = sorted(
            chain(public_posts, friend_posts, foff_posts,),
            key=lambda instance: instance.pubDate, reverse=True)
        return all_visible_posts


class Post(models.Model):
    """Model for representing a Post made by an Author"""

    objects = models.Manager()
    objects_ext = ExtendedPostManager()

    guid = models.CharField(max_length=40, blank=True, default=uuid_import.uuid4, primary_key=True, validators=[UuidValidator()])
    source = models.CharField(max_length=100, blank=True, default='Unknown source')
    origin = models.CharField(max_length=100, blank=True, default='Unknown origin')

    title = models.CharField(max_length=40, blank=True, default='No title')
    description = models.CharField(max_length=40, blank=True, default='No description')
    categories = models.ManyToManyField(Category, blank=True, related_name='tagged_posts')
    content = models.TextField(blank=False)

    # only author or foreign author should be set
    # genericAuthor = models.ForeignKey(GenericUser, null=True, blank=True, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="posts")
    foreign_author = models.ForeignKey(ForeignUser, null=True, blank=True, related_name="posts")

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
    # genericAuthor = models.ForeignKey(GenericUser, null=True, blank=True, related_name="comments")
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

