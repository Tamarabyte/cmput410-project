import json
from rest_framework import serializers
from Hindlebook.models import Post, Comment, Node, Category, Author
from api.serializers import AuthorSerializer
from api.serializers.comment_serializer import CommentSerializer
from api.requests.profile_factory import ProfileRequestFactory
from django.shortcuts import get_object_or_404


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


class PostSerializer(serializers.ModelSerializer):
    """
    A Serializer for the Post Model
    """
    comments = CommentSerializer(many=True, read_only=False)
    author = AuthorSerializer(read_only=False, required=True)
    pubDate = serializers.DateTimeField(required=True)

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """

        # Get the superclass representation
        ret = super(PostSerializer, self).to_representation(instance)

        # Rename 'content_type' to 'content-type'
        content_type = ret.pop('content_type')
        ret['content-type'] = content_type

        return ret

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

            github_id = profileJSON.get('github_id', None)
            about = profileJSON.get('about', None)
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

    def repackage_comment(self, comment_data):
        """
        When you nest serializers, it renames your incoming fields...
        Need to turn them back to the expected... yikes
        """
        author = comment_data.pop('author', None)
        if author is not None:
            author['displayname'] = author['username']
            author.pop('username', None)
            author['id'] = author['uuid']
            author.pop('uuid', None)
            author['host'] = author['node']
            author.pop('node', None)
            comment_data['author'] = author

        return comment_data

    def create(self, validated_data):
        """
        Creates and return a new `Post` instance, given the validated data.
        """

        # Pop nested relationships, we need to handle them separately
        author_data = validated_data.pop('author')
        comment_data = validated_data.pop('comments')
        categories_data = validated_data.pop('categories')

        # Get the Author
        author = self.get_author(author_data)

        # Create the post
        post = Post.objects.create(author=author, **validated_data)

        # Add the categories
        for category in categories_data:
            post.categories.add(category)

        # Create the comments
        for comment_json in comment_data:
            # Have to rename the vars.... this is stupid...
            comment_json = self.repackage_comment(comment_json)

            comment = Comment.objects.filter(guid=comment_json.get('id')).first()
            if comment is None:
                serializer = CommentSerializer(data=comment_json)
                serializer.is_valid(raise_exception=True)
                serializer.save(post=post)

        return post

    def update(self, instance, validated_data):
        """
        Updates an instance of the Post Model
        """
        # Pop nested relationships, we need to handle them separately
        author_data = validated_data.pop('author', None)
        comment_data = validated_data.pop('comments', None)
        categories_data = validated_data.pop('categories', None)

        # Only update the post if it is timestamped as newer than ours
        pubDate = validated_data.get('pubDate', None)
        if pubDate > instance.pubDate:
            # Call Super to update the Post instance
            instance = super(PostSerializer, self).update(instance, validated_data)

        # Update the comments
        for comment_json in comment_data:
            # Have to rename the vars.... this is stupid...
            comment_json = self.repackage_comment(comment_json)

            guid = comment_json.get('guid')
            comment = Comment.objects.filter(guid=guid).first()
            if comment is None:
                # create
                serializer = CommentSerializer(data=comment_json)
                serializer.is_valid(raise_exception=True)
                comment = serializer.save(post=instance)
            else:
                # update
                serializer = CommentSerializer(comment, data=comment_json)
                serializer.is_valid(raise_exception=True)
                comment = serializer.save()

        return instance

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'content_type', 'content',
                  'author', 'categories', 'comments', 'pubDate', 'guid', 'visibility')
