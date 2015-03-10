from django.shortcuts import get_object_or_404
from Hindlebook.models import Post, User
from api.serializers.post_serializer import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status


class PostDetails(APIView):
    """ GET, POST, or PUT an author post """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, guid, format=None):
        # Get the specified Post
        post = get_object_or_404(Post, guid=guid)

        # Serialize
        serializer = PostSerializer(post)

        # Return JSON
        return Response(serializer.data)

    def post(self, request, guid, format=None):
        # Get the specified Post
        post = get_object_or_404(Post, guid=guid)

        # Serialize
        serializer = PostSerializer(post)

        # Return JSON
        return Response(serializer.data)

    def put(self, request, guid, format=None):
        post = get_object_or_404(Post, guid=guid)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthoredPosts(APIView):
    """ GET posts from given author """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uuid, format=None):
        # Get the specified Author
        postAuthor = get_object_or_404(User, uuid=uuid)

        # Get the Author's Posts
        # TODO: FIX ME: change to (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
        posts = postAuthor.getAuthoredPosts()

        # Serialize the Authors Posts
        serializer = PostSerializer(posts, many=True)

        # Return JSON
        return Response({"posts": serializer.data})


class PublicPosts(APIView):
    """ GET all public posts """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        # Filter to get public posts
        serializer = PostSerializer(Post.objects.filter(visibility='PUBLIC'), many=True)

        # Return JSON
        return Response({"posts": serializer.data})


class VisiblePosts(APIView):
    """ GET all posts visbile to the current logged in user """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        # Filter to get public posts
        # TODO: FIX ME: change to (all posts visible to the currently authenticated user)
        serializer = PostSerializer(Post.objects.filter(visibility='PUBLIC'), many=True)

        # Return JSON
        return Response({"posts": serializer.data})
