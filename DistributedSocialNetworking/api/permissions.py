from rest_framework import permissions


class NodeAuthenticatedOrNotRequired(permissions.BasePermission):
    """
    Custom Permissions Class for Nodes
    """
    def has_permission(self, request, view):
        node = request.user

        # Todo: Handle the case where the node does not need permissions

        return node is not None
