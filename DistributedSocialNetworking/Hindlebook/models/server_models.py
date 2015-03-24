from django.db import models
import uuid as uuid_import


class Node(models.Model):
    """Model for representing different servers"""

    # address of the nodes host
    host = models.CharField(max_length=100, blank=False, unique=True)
    # short name for identifying the nodes host
    host_name = models.CharField(max_length=50, blank=True, default='')

    # flags determining the extend of our sharing with this node
    share_posts = models.BooleanField(blank=True, default=True)
    share_images = models.BooleanField(blank=True, default=True)
    require_auth = models.BooleanField(blank=True, default=True)

    # password to access this node
    password = models.CharField(max_length=128, blank=True, default="")

    def __str__(self):
        return self.host


class Settings(models.Model):
    """Model for our server."""

    connection_limit = models.IntegerField(blank=True, default=10)
    local_node = models.OneToOneField(Node, null=True)

    class Meta:
        verbose_name_plural = "Settings"
