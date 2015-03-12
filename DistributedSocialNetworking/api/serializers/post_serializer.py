from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Post, User, Comment, Server, ForeignUser, Node, Category
from api.serializers import AuthorSerializer, ForeignAuthorSerializer
from api.serializers.comment_serializer import CommentSerializer
from django.shortcuts import get_object_or_404
from collections import OrderedDict


class CategorySerializer(serializers.ModelSerializer):
    """A Serializer for the Category Model"""
    class Meta:
        model = Category
        fields = ('tag')


class PostSerializer(serializers.ModelSerializer):
    """A Serializer for the Post Model"""
    comments = CommentSerializer(many=True, read_only=False)
    categories = CategorySerializer(many=True, read_only=False)

    def create(self, validated_data):
        """Create and return a new `Post` instance, given the validated data."""

        print(str(validated_data))

        # Pop nested relationships
        author_data = validated_data.pop('author')
        comment_data = validated_data.pop('comments')
        categories_data = validated_data.pop('categories') # TODO FIX ME: These aren't working?

        print(str(author_data))

        # Get Author/Host info
        uuid = author_data.get('uuid')
        host = author_data.get('node')
        username = author_data.get('username')

        print(str(uuid))
        print(str(host))
        print(str(username))

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
            foreign_user = ForeignUser.objects.get_or_create(node=node, uuid=uuid, username=username)[0]

        # Create the post
        post = Post.objects.create(author=user, foreign_author=foreign_user, **validated_data)

        # # Add the categories
        # for category in categories_data:
        #     print(category)
        #     cat = Category.objects.get_or_create(tag = category)
        #     print(cat)
        #     post.categories.add(cat)

        # Create the comments
        for comment in comment_data:
            Comment.objects.create(author=user, foreign_author=foreign_user, post=post, **comment)

        return post

    def update(self, instance, validated_data):
        """Updates an instance of the Post Model"""
        # TODO: FIX ME: Do something with comments?? Waiting on Hindle Response
        comment_data = validated_data.pop('comments')
        categories_data = validated_data.pop('categories')
        return super(PostSerializer, self).update(instance, validated_data)

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'content_type', 'content',
                  'categories', 'comments', 'pubDate', 'guid', 'visibility')


class LocalPostSerializer(PostSerializer):
    """A Serializer for a Post made by a Local Author"""
    author = AuthorSerializer(read_only=False)

    def update(self, instance, validated_data):
        """
        Updates an instance of the Post Model
        """
        validated_data.pop('author')
        return super(LocalPostSerializer, self).update(instance, validated_data)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ('author',)


class ForeignPostSerializer(PostSerializer):
    """A Serializer for a Post made by a Foreign Author"""
    author = ForeignAuthorSerializer(read_only=False, source='foreign_author')

    def create(self, validated_data):
        """
        Creates an instance of the Post Model
        """
        # Rename 'foreign_author' to 'author'
        foreign_author = validated_data.pop('foreign_author')
        validated_data['author'] = foreign_author

        return super(ForeignPostSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        """
        Updates an instance of the Post Model
        """
        validated_data.pop('foreign_author')

        return super(ForeignPostSerializer, self).update(instance, validated_data)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ('author',)
