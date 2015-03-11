from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Post, User, Comment, Server, ForeignUser, Node, Category
from api.serializers import AuthorSerializer
from api.serializers.comment_serializer import CommentSerializer
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):
    """A Serializer for the Category Model"""
    class Meta:
        model = Category
        fields = ('tag')


class PostSerializer(serializers.ModelSerializer):
    """A Serializer for the Post Model"""
    author = AuthorSerializer(read_only=False)
    comments = CommentSerializer(many=True, read_only=False)
    categories = CategorySerializer(many=True, read_only=False)

    def create(self, validated_data):
        """Create and return a new `Post` instance, given the validated data."""

        # Pop nested relationships
        author_data = validated_data.pop('author')
        comment_data = validated_data.pop('comments')
        categories_data = validated_data.pop('categories') # TODO FIX ME: These aren't working?

        # Get Author/Host info
        author_id = author_data.get('uuid')
        host = author_data.get('node')

        # Check whether this is a local or foreign post
        server = Server.objects.filter(host=host).first()
        if server is not None:
            # It's local! Get the user, or 404 if the user doesn't exist
            # TODO: FIX ME 400 instead??
            user = get_object_or_404(User, uuid=author_id)
        else:
            # Foreign Node: Add it if we haven't seen it before
            Node.objects.get_or_create(host=host)
            # Add the ForeignUser if we haven't seen them before
            user = ForeignUser.objects.get_or_create(**author_data)


        # Create the post
        post = Post.objects.create(author=user, **validated_data)

        # # Add the categories
        # for category in categories_data:
        #     print(category)
        #     cat = Category.objects.get_or_create(tag = category)
        #     print(cat)
        #     post.categories.add(cat)

        # Create the comments
        for comment in comment_data:
            Comment.objects.create(author=user, post=post, **comment)

        return post

    def update(self, instance, validated_data):
        """Updates an instance of the Post Model"""
        # TODO: FIX ME: Do something with comments?? Waiting on Hindle Response
        author_data = validated_data.pop('author')
        comment_data = validated_data.pop('comments')
        categories_data = validated_data.pop('categories')
        return super(PostSerializer, self).update(instance, validated_data)

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'content_type', 'content', 'author', 'categories',
                  'comments', 'pubDate', 'guid', 'visibility')
