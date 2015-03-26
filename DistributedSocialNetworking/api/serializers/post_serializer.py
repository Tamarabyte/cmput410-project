import json
# import requests
# from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Post, Comment, Node, Category, Author
from api.serializers import AuthorSerializer
from api.serializers.comment_serializer import CommentSerializer
from api.requests import ProfileRequestFactory
from django.shortcuts import get_object_or_404
# import datetime
# import dateutil.parser


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
    pubDate = serializers.DateTimeField()

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

    def create_comments(self, post, comment_data):
        """
        Creates the comments for `post` stored in `comment_data`
        """
        for comment in comment_data:
            author = comment.pop('author', None)
            if author is None:
                raise serializers.ValidationError('The Author field of a Comment is required.')
            author = self.get_author(author)
            Comment.objects.create(author=author, post=post, **comment)

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
        self.create_comments(post, comment_data)

        return post

    def update(self, instance, validated_data):
        """Updates an instance of the Post Model"""

        # Pop nested relationships, we need to handle them separately
        author_data = validated_data.pop('author', None)
        comment_data = validated_data.pop('comments', None)

        # Call Super to create the Post instance
        instance = super(PostSerializer, self).update(instance, validated_data)

        # Create the comments, if provided
        if comment_data is not None:
            self.create_comments(instance, comment_data)

        return instance

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'content_type', 'content',
                  'author', 'categories', 'comments', 'pubDate', 'guid', 'visibility')


class NonSavingPostSerializer(serializers.ModelSerializer):
    """
    A Serializer for the Post Model that doesn't save
    """
    comments = CommentSerializer(many=True, read_only=False)
    author = AuthorSerializer(read_only=False, required=True)
    pubDate = serializers.DateTimeField()
    categories = serializers.ListField(child=serializers.CharField(max_length=15))

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

            github_id = profileJSON.get('github_id', None)
            about = profileJSON.get('about', None)
            username = profileJSON.get('username', username)

            author = Author(uuid=uuid, node=node, username=username,
                            github_id=github_id, about=about)

        return author

    def create_comments(self, post, comment_data):
        """
        Creates the comments for `post` stored in `comment_data`
        """

        # [OrderedDict([('author', OrderedDict([('username', 'mark2'), ('node', 'localhost:8080'), ('uuid', '1611693a-6167-4b89-8916-0ab40b8820cc')])), ('comment', "Mark2's commetn!"), ('guid', 'ad73cd02-5c2f-4a79-9675-65aa5a2c8c23')])]

        # [{"author": {"username": "mark2", "node": "localhost:8080", "uuid": "1611693a-6167-4b89-8916-0ab40b8820cc"}, "comment": "Mark2's commetn!", "guid": "ad73cd02-5c2f-4a79-9675-65aa5a2c8c23"}]

        if comment_data is None:
            return

        for comment in comment_data:
            author = comment.pop('author', None)
            if author is None:
                raise serializers.ValidationError('The Author field of a Comment is required.')
            author = self.get_author(author)
            post.comments.add(Comment(author=author, post=post, **comment))

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
        post = Post(author=author, **validated_data)

        # Add the categories
        for category in categories_data:
            post.categories.add(category)

        # Create the comments
        self.create_comments(post, comment_data)

        return post

    def update(self, instance, validated_data):
        """
        Not Supported
        """
        return None

    def validate_categories(self, value):
        categories = value

        for cat in categories:
            Category.objects.get_or_create(tag=cat)
        return value

    def validate_comments(self, value):
        pass

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'content_type', 'content',
                  'author', 'categories', 'comments', 'pubDate', 'guid', 'visibility')

