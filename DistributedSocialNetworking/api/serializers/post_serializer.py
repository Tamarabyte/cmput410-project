from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Post, User, Comment, Server, ForeignUser, Node, Category
from api.serializers import AuthorSerializer, ForeignAuthorSerializer
from api.serializers.comment_serializer import CommentSerializer
from django.shortcuts import get_object_or_404
from collections import OrderedDict


class PostSerializer(serializers.ModelSerializer):
    """
    A Serializer for the Post Model
    """
    comments = CommentSerializer(many=True, read_only=False)
    author = AuthorSerializer(read_only=False, required=True)
    foreign_author = ForeignAuthorSerializer(read_only=False, required=False)

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """

        # Get the superclass representation
        ret = super(PostSerializer, self).to_representation(instance)

        # Pop foreign_author... we don't want to print that
        foreign_author = ret.pop('foreign_author', None)

        # Rename 'foreign_author' to 'author' if needed
        author = ret.get('author', None)
        if author is None:
            ret['author'] = foreign_author

        return ret

    def get_author(self, author_data):
        """
        gets the local/foreign authors and adds the foreign user/node if necessry
        """
        if author_data is None:
            return None

        # Get Author/Host info
        uuid = author_data.get('uuid')
        host = author_data.get('node')
        username = author_data.get('username')

        user = None
        foreign_user = None
        # Check whether this is a local or foreign post
        server = Server.objects.filter(host=host).first()
        if server is not None:
            # It's local! Get the user, or 404 if the user doesn't exist
            # TODO: FIX ME 400 instead??
            user = get_object_or_404(User, uuid=uuid)
        else:
            # Foreign Node: Add it if we haven't seen it before
            node = Node.objects.get_or_create(host=host)[0]
            # Add the ForeignUser if we haven't seen them before
            foreign_user = ForeignUser.objects.get_or_create(node=node, uuid=uuid,
                                                             username=username)[0]

        return (user, foreign_user)

    def create_comments(self, post, comment_data):
        """
        Creates the comments for `post` stored in `comment_data`
        """
        for comment in comment_data:
            print(comment)
            author, foreign_author = self.get_author(comment.pop('author'))
            Comment.objects.create(author=author, foreign_author=foreign_author,
                                   post=post, **comment)

    def create(self, validated_data):
        """
        Creates and return a new `Post` instance, given the validated data.
        """

        # Pop nested relationships, we need to handle them separately
        author_data = validated_data.pop('author')
        comment_data = validated_data.pop('comments')
        categories_data = validated_data.pop('categories')

        # Get the Author
        author, foreign_author = self.get_author(author_data)

        # Create the post
        post = Post.objects.create(author=author, foreign_author=foreign_author, **validated_data)

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
                  'author', 'categories', 'comments', 'pubDate', 'guid', 'visibility',
                  'foreign_author')
