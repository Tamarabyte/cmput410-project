from django.db import models
import uuid as uuid_import


class ExtendedNodeManager(models.Manager):
    def getActiveNodes(self):
        return self.get_queryset().filter(is_connected=True)
    

class Node(models.Model):
    """Model for representing different servers"""

    # extended manager with some utility methods
    objects = ExtendedNodeManager()
    
    # address of the nodes host
    host = models.CharField(max_length=100, blank=False, unique=True, help_text="URL of the host. ex. http://hindlebook.tamarabyte.com ")
    # short name for identifying the nodes host
    host_name = models.CharField(verbose_name="username", max_length=50, blank=True, default='', help_text="Username/short identifier of host. ex. hindlebook")

    # flags determining the extend of our sharing with this node
    is_connected = models.BooleanField(verbose_name="connect_with", blank=True, default=False, help_text="Whether or not we actively pull posts/authors from this node.")
    share_posts = models.BooleanField(blank=True, default=True)
    share_images = models.BooleanField(blank=True, default=True)
    require_auth = models.BooleanField(blank=True, default=True)

    # password to access this node
    password = models.CharField(max_length=128, blank=True, default="", help_text="Password this node connects to us with.")

    our_username = models.CharField(verbose_name="username", max_length=128, blank=True, default="", help_text="Username this node wants from us.")
    our_password = models.CharField(verbose_name="password", max_length=128, blank=True, default="", help_text="Password this node wants from us.")

    team_number = models.IntegerField(blank=False, default=9)

    def __str__(self):
        return self.host


class Settings(models.Model):
    """Model for our server."""

    connection_limit = models.IntegerField(blank=True, default=10)
    node = models.ForeignKey(Node, null=True, blank=False, default=1)

    class Meta:
        verbose_name_plural = "Settings"
