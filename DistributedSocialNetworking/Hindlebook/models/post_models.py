from Hindlebook.models.user_models import Author
from Hindlebook.models import UuidValidator
from datetime import datetime
from django.db import models
from django.db.models import Q
from itertools import chain
import uuid as uuid_import
import functools
import operator
from django.utils import timezone


class Category(models.Model):
    tag = models.CharField(max_length=15, null=False, blank=False, primary_key=True)

    def __str__(self):
        return self.tag

    class Meta():
        verbose_name = "Tags"
        verbose_name_plural = "Tags"
        ordering = ['tag']


class ExtendedPostManager(models.Manager):

    def get_all_visibile_posts(self, active_author, reversed=True, min_time=None):
        """Gets all the posts visible to the provided user"""
        #  Get list of friends
        friends = active_author.getFriends()
        #  Get list of friends of friends
        friends_ext = active_author.getFriendsOfFriends()

        #  This is a safe way to add values to the filters that could be None
        q_list = [Q()]
        if min_time is not None:
            q_list.append(Q(pubDate__gt=min_time))
        q_reduced = functools.reduce(operator.and_, q_list)

        my_posts = Post.objects.filter(q_reduced, author=active_author)  # My posts
        public_posts = Post.objects.filter(q_reduced, visibility="PUBLIC").exclude(author=active_author)  # Public Posts
        friend_posts = Post.objects.filter(q_reduced, visibility="FRIENDS", author__in=friends).exclude(author=active_author)  # Friend Posts from my frineds
        foff_posts = Post.objects.filter(q_reduced, visibility="FOAF", author__in=friends_ext).exclude(author=active_author)  # FOAF posts from FOAFS

        #  Merge lists
        all_visible_posts = sorted(
            chain(my_posts, public_posts, friend_posts, foff_posts,),
            key=lambda instance: instance.pubDate, reverse=reversed)
        return all_visible_posts

    def get_profile_visibile_posts(self, active_author, page_author):
        """Get all the posts made by page_author that are visible to active_author"""

        #  Is the active user the user they are looking at
        if active_author == page_author:
            return Post.objects.filter(author=page_author).order_by('-pubDate')

        #  Get list of friends
        friends = active_author.getFriends()
        #  Get list of friends of friends
        friends_ext = active_author.getFriendsOfFriends()

        #  Get the public posts by the page_author
        public_posts = Post.objects.filter(visibility="PUBLIC", author=page_author)
        friend_posts = {}
        foff_posts = {}
        #  Is the page_author a friend then get their friends only posts
        if page_author in friends:
            friend_posts = Post.objects.filter(visibility="FRIENDS", author=page_author)
        #  Is the page_author a friend of a friend then get their FOAF only posts
        if page_author in friends_ext:
            foff_posts = Post.objects.filter(visibility="FOAF", author=page_author)

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
    source = models.CharField(max_length=100, blank=True, default='')
    origin = models.CharField(max_length=100, blank=True, default='')

    title = models.CharField(max_length=40, blank=False, default='')
    description = models.CharField(max_length=40, blank=True, default='')
    categories = models.ManyToManyField(Category, blank=True, related_name='tagged_posts')
    content = models.TextField(blank=False)

    author = models.ForeignKey(Author, related_name="posts")

    pubDate = models.DateTimeField('date published', default=timezone.now, db_index=True)

    content_type_choices = (("text/plain", "Text"), ("text/x-markdown", "Markdown"), ("text/html", "HTML"))
    content_type = models.CharField(max_length=15, blank=True, choices=content_type_choices, default="text/plain")

    visibility_choices = (("PUBLIC", "Public"), ("FOAF", "Friends of Friends Only"), ("FRIENDS", "Friends Only"), ("PRIVATE", "Private"), ("SERVERONLY", "Server Only"))
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

    author = models.ForeignKey(Author, related_name="comments")

    comment = models.CharField(max_length=2048)
    pubDate = models.DateTimeField('date published', default=timezone.now, db_index=True)

    def save(self, *argv, **kwargs):
        if Post.objects.filter(guid=self.post) is not None:
            super(Comment, self).save(*argv, **kwargs)
            return True
        return False

    def __str__(self):
        return str(self.guid)


class Image(models.Model):

    """Model for representing an Image attached to Posts"""
    attached_to = models.ForeignKey(Post, null=False)
    image = models.ImageField(null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image
