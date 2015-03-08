from django.db import models
from django.conf import settings
import uuid

class Post(models.Model):
    """Model for representing a Post made by an Author"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    uuid = models.CharField(max_length=40, blank=False, default=uuid.uuid4)
    title = models.CharField(max_length=40, blank=True, default='No title')
    description = models.CharField(max_length=40, blank=True, default='No description')
    content_type = models.CharField(max_length=40, blank=True, default='text/plain')
    source = models.CharField(max_length=100, blank=True, default='Unknown source')
    origin = models.CharField(max_length=100, blank=True, default='Unknown origin')
		
	# Edited by Rob Hackman March 7th
	# Added field for privacy on posts, privacy settings are as follows
	# 0 - Private to me
	# 1 - Private to one other author
	# 2 - Private to my friends
	# 3 - Private to friends of friends
	# 4 - private to friends on my host
	# 5 - Public
    privacy_choices = ((0,"Self Only"),
					    (1,"Selected author"),
					    (2,"Friends"),
					    (3,"Friends of Friends"),
					    (4,"Friends on host"),
					    (5,"Public"))
    privacy = models.IntegerField(default=5,max_length=1,choices=privacy_choices)
	# Need to add some way to specify for privacy setting 1 who the other author is

    def __str__(self):
		# Edited by Rob Hackman March 7th 
		# Ultimately this should probably return some sort of HTML
		# for displaying the post in case it's  got a picture etc.
        return str(self.text)

    # Get the comments for this Post
    def getComments(self):
        return self.comments.all()


class Comment(models.Model):
    """Model for representing a Comment on a Post made by an Author"""
    post = models.ForeignKey(Post, related_name="comments")
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

