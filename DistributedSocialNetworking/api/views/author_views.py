from Hindlebook.models import Author
from api.serializers import AuthorSerializer, UserEditSerializer, ProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions


class AllowReadonlyOrAdminOrSelf(permissions.BasePermission):
    """
    Allow access to admin users or the user himself.
    """

    def has_permission(self, request, view):
        """ Readonly or Admin """
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        """ Readonly or Admin or editing self """
        if request.method in permissions.SAFE_METHODS:
            return True
        if all([request.user, request.user.is_staff]):
            return True
        elif all([request.user, type(obj) == type(request.user), obj == request.user]):
            return True

        return True


class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for interacting with local authors.
    checkout routers.CustomSimpleRouter for it's bindings.

    includes:
     - get /authors : returns a list of authors in JSON format
     - get /author/uuid : returns author in JSON format
     - put /author/uuid : requires authentication
    """

    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowReadonlyOrAdminOrSelf,)
    serializer_class = AuthorSerializer
    profileSerializer_class = ProfileSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Author.objects.all()

    def retrieve(self, request, uuid=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, uuid=uuid)
        serializer = self.profileSerializer_class(user)
        return Response(serializer.data)

    def update(self, request, uuid=None, *args, **kwargs):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, uuid=uuid)

        # validate and perform partial update
        serializer = UserEditSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_excetion=True)
        serializer.save()
        self.perform_update(serializer)
        return Response(serializer.data)
