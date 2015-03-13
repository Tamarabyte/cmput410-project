from Hindlebook.models import Post, User, Server, Category
from api.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.shortcuts import get_object_or_404


class PostDetails(APIView):
    """
    GET, POST, or PUT an author post
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def add_categories(self, data):
        """
        Adds Categories to the database if necessary
        """
        categories = data.get('categories', None)
        for category in categories:
            if not Category.objects.filter(tag=category).exists():
                Category.objects.create(tag=category)

    def put_as_update(self, request, guid):
        """
        Updates an instance of Post
        """
        # Fetch the post
        post = Post.objects.get(guid=guid)

        # Purge old comments, if necessary
        if request.data.get('comments', None) is not None:
            post.comments.all().delete()

        # Serialize the post
        serializer = PostSerializer(post, data=request.data)
        return (serializer, status.HTTP_200_OK)

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
            serializer, status_code = self.put_as_update(request, guid)
        else:
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
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uuid, format=None):
        # Get the specified Author
        pageAuthor = get_object_or_404(User, uuid=uuid)

        # Get the Author's Posts
        posts = Post.objects_ext.get_profile_visibile_posts(self.request.user, pageAuthor)

        # Serialize all of the posts
        serializer = PostSerializer(posts, many=True)

        # Return JSON
        return Response({"posts": serializer.data})


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
        serializer = PostSerializer(posts, many=True)

        # Return JSON
        return Response({"posts": serializer.data})


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
        serializer = PostSerializer(posts, many=True)

        # Return JSON
        return Response({"posts": serializer.data})
