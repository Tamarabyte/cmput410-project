from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

class NodeAuthenticatedOrNotRequired(permissions.BasePermission):
    """
    Custom Permissions Class for Nodes
    """
    def has_permission(self, request, view):

        # TODO FIXME: Handle the case where the node does not need permissions
        # Should be a flat return True

        # Failed Authentication
        if(isinstance(request.user, AnonymousUser)):
            return False

        return True
