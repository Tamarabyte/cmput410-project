from rest_framework import serializers
from Hindlebook.models import Comment, Node, Author
from api.serializers import AuthorSerializer
from api.requests.profile_factory import ProfileRequestFactory


def getForeignProfile(uuid, node):
    """
    Fetches the profile for the foreign user specified by uuid from the specfied node
    """
    author = None

    request = ProfileRequestFactory.create(node)
    response = request.get(uuid)

    if(response.status_code != 200):
        # Node not reachable or some other mishap
        print(response.content)
        print("Node %s returned us status code %s!!!" % (node.host_name, response.status_code))
        return None

    return response.json()


class CommentSerializer(serializers.ModelSerializer):

    """A Serializer for the Comment Model"""
    author = AuthorSerializer(read_only=False, required=True)
    guid = serializers.CharField(max_length=40, required=True)
    pubDate = serializers.DateTimeField()

    def get_author(self, author_data):
        """
        gets the authors and adds the user/node if necessry
        """
        if author_data is None:
            return None

        # Get Author/Host info
        uuid = author_data.get('uuid')
        host = author_data.get('node')
        username = author_data.get('username')

        node = Node.objects.filter(host=host).first()
        if node is None:
            raise serializers.ValidationError('Unknown Host: %s' % host)

        author = Author.objects.filter(uuid=uuid).first()
        if author is None:
            # New foreign author
            profileJSON = getForeignProfile(uuid, node)
            if profileJSON is None:
                profileJSON = {}

            github_id = profileJSON.get('github_id', "")
            about = profileJSON.get('about', "")
            username = profileJSON.get('username', username)

            author = Author.objects.create(uuid=uuid, node=node, username=username,
                                           github_id=github_id, about=about)

        elif author.user is None:
            # Existing Foreign Author, update them
            profileJSON = getForeignProfile(uuid, node)
            if profileJSON is None:
                profileJSON = {}

            github_id = profileJSON.get('github_id', author.github_id)
            about = profileJSON.get('about', author.about)
            username = profileJSON.get('username', username)

            author.username = username
            author.github_id = github_id
            author.about = about
            author.save()

        return author

    def create(self, validated_data):
        """
        Creates and return a new `Comment` instance, given the validated data.
        """
        # Pop nested relationships, we need to handle them separately
        author_data = validated_data.pop('author', None)
        validated_data['author'] = self.get_author(author_data)

        return super(CommentSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        """
        Updates and returns an instance of the `Comment` Model with validated data
        """

        # Pop nested relationships, we need to handle them separately
        author_data = validated_data.pop('author', None)
        pubDate = validated_data.get('pubDate', None)

        # Only Update comments if they are newer
        if pubDate > instance.pubDate:
            # Set the author
            validated_data['author'] = self.get_author(author_data)
            # Call Super to update the Comment instance
            instance = super(CommentSerializer, self).update(instance, validated_data)

        return instance

    class Meta:
            model = Comment
            fields = ('author', 'comment', 'pubDate', 'guid')
