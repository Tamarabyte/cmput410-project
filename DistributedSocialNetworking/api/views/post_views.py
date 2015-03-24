from Hindlebook.models import Post, Category, Node, Author
from api.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, exceptions, HTTP_HEADER_ENCODING
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404


def get_uuid_from_header(request):
    """
    Return request's 'x-uuid:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    user = request.META.get('HTTP_UUID', b'')
    if isinstance(user, type('')):
        # Work around django test client oddness
        user = user.encode(HTTP_HEADER_ENCODING)

    user_parts = user.decode(HTTP_HEADER_ENCODING).split(':')

    if not user_parts or user_parts[0] == '':
        msg = _('Invalid `uuid` header. No `uuid` header provided.')
        raise exceptions.AuthenticationFailed(msg)

    if len(user_parts) != 1:
        msg = _('Invalid `uuid` header format. Expect `uuid`')
        raise exceptions.AuthenticationFailed(msg)

    return user_parts[0]


def get_author(uuid, node):
    try:
        author = Author.objects.get(uuid=uuid)
    except Author.DoesNotExist:
        author = Author.objects.create(uuid=uuid, username="DummyUsername", node=node)   # TODO: FIX ME: make a request for the username

    return author


class PostDetails(APIView):
    """
    GET, POST, or PUT an author post
    """

    def add_categories(self, data):
        """
        Adds Categories to the database if necessary
        """
        categories = data.get('categories', None)
        if categories is not None:
            for category in categories:
                if not Category.objects.filter(tag=category).exists():
                    Category.objects.create(tag=category)

    def get(self, request, guid, format=None):
        """
        Get, serialize, and return an instance of Post
        """
        post = get_object_or_404(Post, guid=guid)
        serializer = PostSerializer(post)
        return Response({"posts": [serializer.data]})

    def post(self, request, guid, format=None):
        """
        Get, serialize, and return an instance of Post
        """
        if Post.objects.filter(guid=guid).exists():
            return Response({"error": ["Post already exists."]}, status=status.HTTP_400_BAD_REQUEST)

        # Rename `content-type` to content_type
        content_type = request.data.pop('content-type', None)
        if content_type is not None:
            request.data['content_type'] = content_type

        # Serialize the data
        serializer = PostSerializer(data=request.data)

        # Validate the Serializer
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"posts": [serializer.data]}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, guid, format=None):
        """
        Creates or Updates an instance of Post
        """

        # Rename `content-type` to content_type
        content_type = request.data.pop('content-type', None)
        if content_type is not None:
            request.data['content_type'] = content_type

        # Add new categories to our database... Yeah...
        self.add_categories(request.data)

        if Post.objects.filter(guid=guid).exists():
            # Put as Update
            # Fetch the post
            post = Post.objects.get(guid=guid)

            # Purge old comments, if necessary
            if request.data.get('comments', None) is not None:
                post.comments.all().delete()

            # Serialize the post
            serializer = PostSerializer(post, data=request.data, partial=True)
            status_code = status.HTTP_200_OK
        else:
            # Put as Create
            serializer = PostSerializer(data=request.data)
            status_code = status.HTTP_201_CREATED

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"posts": [serializer.data]}, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthoredPosts(APIView):
    """
    GET posts from given author
    """
    def get(self, request, uuid, format=None):
        # Get the specified Author
        pageAuthor = get_object_or_404(Author, uuid=uuid)

        # Get info from request
        uuid = get_uuid_from_header(request)
        node = request.user

        # Get the Author's Posts
        author = get_author(uuid, node)
        posts = Post.objects_ext.get_profile_visibile_posts(author, pageAuthor)

        # Serialize all of the posts
        serializer = PostSerializer(posts, many=True)

        # Return JSON
        return Response({"posts": serializer.data})


class PublicPosts(APIView):
    """
    GET all public posts
    """

    # Because public
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        # Filter to get public posts
        posts = Post.objects.filter(visibility='PUBLIC')

        # Serialize all of the posts
        serializer = PostSerializer(posts, many=True)

        # Return JSON
        return Response({"posts": serializer.data})


class VisiblePosts(APIView):
    """
    GET all posts visbile to the current logged in user
    """

    def get(self, request, format=None):
        # Get info from request
        uuid = get_uuid_from_header(request)
        node = request.user

        # Filter to get all posts visible to the currently authenticated user
        author = get_author(uuid, node)
        posts = Post.objects_ext.get_all_visibile_posts(author)

        # Serialize all of the posts
        serializer = PostSerializer(posts, many=True)

        # Return JSON
        return Response({"posts": serializer.data})
