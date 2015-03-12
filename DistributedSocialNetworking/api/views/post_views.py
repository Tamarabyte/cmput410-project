from Hindlebook.models import Post, User, Server, Category
from api.serializers import LocalPostSerializer, ForeignPostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.shortcuts import get_object_or_404


def get_serializer_class(author, host=None):
        """
        Returns the correct Post serializer class based
        on local/foreign author status
        """
        if host is not None:
            if Server.objects.filter(host=host).first() is None:
                serializer = ForeignPostSerializer
            else:
                serializer = LocalPostSerializer
        elif author is None:
            serializer = ForeignPostSerializer
        else:
            serializer = LocalPostSerializer

        return serializer


def serialize(post):
    """
    Serializes a Post instance
    """
    serializer_class = get_serializer_class(post.author)
    return serializer_class(post)


class PostDetails(APIView):
    """
    GET, POST, or PUT an author post
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, guid, format=None):
        """
        Get, serialize, and return an instance of Post
        """
        post = get_object_or_404(Post, guid=guid)

        serializer_class = get_serializer_class(post.author)
        serializer = serializer_class(post)

        return Response({"posts": [serializer.data]})

    def post(self, request, guid, format=None):
        """
        Get, serialize, and return an instance of Post
        """
        return self.get(request, guid)

    def put(self, request, guid, format=None):
        """
        Creates or Updates an instance of Post
        """

        # Add new categories to our database... Yeah...
        categories = request.data.get('categories', None)
        for category in categories:
            if not Category.objects.filter(tag=category).exists():
                Category.objects.create(tag=category)

        if Post.objects.filter(guid=guid).exists():
            # PUT as update

            # Get the serializer
            host = request.data.get('author').get('host')
            serializer_class = get_serializer_class(None, host)
            # Serialize the post
            post = Post.objects.get(guid=guid)
            serializer = serializer_class(post, data=request.data)
            status_code = status.HTTP_200_OK
        else:
            # PUT as create

            # Get the serializer
            host = request.data.get('author').get('host')
            serializer_class = get_serializer_class(None, host)

            # Serialize the post data
            serializer = serializer_class(data=request.data)
            status_code = status.HTTP_201_CREATED

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"posts": [serializer.data]}, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthoredPosts(APIView):
    """
    GET posts from given author
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uuid, format=None):
        # Get the specified Author
        pageAuthor = get_object_or_404(User, uuid=uuid)

        # Get the Author's Posts
        posts = Post.objects_ext.get_profile_visibile_posts(self.request.user, pageAuthor)

        # Serialize all of the posts
        data = [serialize(post).data for post in posts]

        # Return JSON
        return Response({"posts": data})


class PublicPosts(APIView):
    """
    GET all public posts
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        # Filter to get public posts
        posts = Post.objects.filter(visibility='PUBLIC')

        # Serialize all of the posts
        data = [serialize(post).data for post in posts]

        # Return JSON
        return Response({"posts": data})


class VisiblePosts(APIView):
    """
    GET all posts visbile to the current logged in user
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        # Filter to get all posts visible to the currently authenticated user
        posts = Post.objects_ext.get_all_visibile_posts(self.request.user)

        # Serialize all of the posts
        data = [serialize(post).data for post in posts]

        # Return JSON
        return Response({"posts": data})
