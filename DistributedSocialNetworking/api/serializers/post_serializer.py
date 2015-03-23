from django.forms import widgets
from rest_framework import serializers
from Hindlebook.models import Post, Comment, Node, Category, Author
from api.serializers import AuthorSerializer
from api.serializers.comment_serializer import CommentSerializer
from django.shortcuts import get_object_or_404


class PostSerializer(serializers.ModelSerializer):
    """
    A Serializer for the Post Model
    """
    comments = CommentSerializer(many=True, read_only=False)
    author = AuthorSerializer(read_only=False, required=True)

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
        gets the local/foreign authors and adds the foreign user/node if necessry
        """
        if author_data is None:
            return None

        # Get Author/Host info
        uuid = author_data.get('uuid')
        host = author_data.get('node')
        username = author_data.get('username')

        author = Author.object.filter(uuid=uuid).first()

        if author is None:
            # New foreign author
            author = Author(uuid=uuid, host=host, username=username)

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
