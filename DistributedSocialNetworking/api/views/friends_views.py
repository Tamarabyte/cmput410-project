from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import FriendQuerySerializer
from Hindlebook.models import Author


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
            try:
                author2 = Author.objects.get(uuid=authorID2)
                if author2 in friends_set:
                    friends.append(authorID2)
            except:
                pass

        return Response({"query": "friends", "author": authorID1, "friends": friends})