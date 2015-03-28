from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import FriendQuerySerializer, FriendRequestSerializer
from api.requests.friend_request_factory import FriendRequestFactory
from Hindlebook.models import Author
from Hindlebook.utilites import Logger
logger = Logger()


class FriendQuery(APIView):
    """
    POST a friend query
    """
    def post(self, request, authorID1, format=None):
        # Validate the request body
        serializer = FriendQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Verify URL UUID matches request UUID
        if (str(authorID1) != str(data.get('author'))):
            return Response({"author": "AuthorUUID in URL does not match request UUID"},
                            status.HTTP_400_BAD_REQUEST)

        # Fetch the Author
        try:
            author1 = Author.objects.get(uuid=authorID1)
        except Author.DoesNotExist:
            return Response({"author": "Author Not Found."}, status.HTTP_404_NOT_FOUND)

        friends = []
        friends_set = author1.getFriends()

        # Compare each friend in the request
        for authorID2 in data.get('authors'):
                author2 = Author.objects.get(uuid=authorID2)
                if author2 in friends_set:
                    friends.append(authorID2)

        return Response({"query": "friends", "author": authorID1, "friends": friends})


class Friend2Friend(APIView):
    """
    GET a friend2friend query
    """
    def get(self, request, authorID1, authorID2, format=None):
        try:
            author1 = Author.objects.get(uuid=authorID1)
            author2 = Author.objects.get(uuid=authorID2)

            if (author2 in author1.getFriends() and author1 in author2.getFriends()):
                friends = "YES"
            else:
                friends = "NO"

        except Author.DoesNotExist:
            friends = "NO"

        return Response({"query": "friends", "authors": [authorID1, authorID2], "friends": friends})


class FriendRequest(APIView):
    """
    POST a friend request
    """
    def echo_request(author, friend):
        """
        Echo friend request to foreign author's node
        If it fails, we don't really care so we bite it.
        """
        request = FriendRequestFactory.create(friend.node)
        try:
            response = request.post(author, friend)
            if response.status_code != 200:
                logger.log("HTTP %s returned from %s on friend request echo." % (response.status_code, node.host))
        except NotImplementedError:
            logger.log("Node %s NotImplementedError on friend request echo." % (node.host))

    def post(self, request, format=None):
        # Validate the request body
        serializer = FriendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author = serializer.validated_data['author']
        friend = serializer.validated_data['friend']

        if author.isForeign() and friend.isForeign():
            return Response({"error": "We aren't a matchmaking service for foreign authors. Try OKcupid?"},
                            status=status.HTTP_400_BAD_REQUEST)
        if friend.isForeign():
            # Echo request to foreign Author's Node
            self.echo_request(author, friend)

        if friend not in author.friends.all():
            author.friends.add(friend)

        if (friend not in author.follows.all()):
            author.follows.add(friend)

        return Response()


class FollowRequest(APIView):
    """
    POST a follow query
    """
    def post(self, request, format=None):
        # Validate the request body
        serializer = FriendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author = serializer.validated_data['author']
        friend = serializer.validated_data['friend']

        if author.isForeign() and friend.isForeign():
            return Response({"error": "We aren't a matchmaking service for foreign authors. Try OKcupid?"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Form the followship
        if (friend not in author.follows.all()):
            author.follows.add(friend)

        return Response()


class UnfollowRequest(APIView):
    """
    POST a unfollow query
    """
    def post(self, request, format=None):
        # Validate the request body
        serializer = FriendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author = serializer.validated_data['author']
        friend = serializer.validated_data['friend']

        if author.isForeign() and friend.isForeign():
            return Response({"error": "We aren't a matchmaking service for foreign authors. Try OKcupid?"},
                            status=status.HTTP_400_BAD_REQUEST)

        if (friend in author.follows.all()):
            author.follows.remove(friend)

        return Response()


class UnfriendRequest(APIView):
    """
    POST an unfriend query
    """

    def post(self, request, format=None):
        # Validate the request body
        serializer = FriendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author = serializer.validated_data['author']
        friend = serializer.validated_data['friend']

        if author.isForeign() and friend.isForeign():
            return Response({"error": "We aren't a matchmaking service for foreign authors. Try OKcupid?"},
                            status=status.HTTP_400_BAD_REQUEST)

        # If someone requsets an unfriend this is either a
        # cancellation of a friend request, or termination
        # of a friend relationship, so we have to remove from
        # the author from the friends list of friends if it exists
        # to terminate an existing friend relationship, not leave
        # a hanging friend request from the friend immediately
        # after termination of their relationship.
        if (friend in author.friends.all()):
            author.friends.remove(friend)
        if (author in friend.friends.all()):
            friend.friends.remove(author)

        return Response()
