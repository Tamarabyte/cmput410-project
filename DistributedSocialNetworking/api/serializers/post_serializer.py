import json
from rest_framework import serializers
from Hindlebook.models import Post, Comment, Node, Category, Author
from api.serializers import AuthorSerializer
from api.serializers.comment_serializer import CommentSerializer
from api.serializers.utils import get_author
from django.shortcuts import get_object_or_404


class PostSerializer(serializers.ModelSerializer):
    """
    A Serializer for the Post Model
    """
    comments = CommentSerializer(many=True, read_only=False)
    author = AuthorSerializer(read_only=False, required=True)
    pubDate = serializers.DateTimeField(required=True)

    def __init__(self, *args, **kwargs):
        # We need to add the categories to the DB before validation
        data = kwargs.get('data', None)
        if data is not None:
            categories = data.get('categories', None)
            if categories is not None:
                for category in categories:
                    Category.objects.get_or_create(tag=category)

        super(PostSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = super(PostSerializer, self).to_representation(instance)

        # Rename 'content_type' to 'content-type'
        content_type = ret.pop('content_type')
        ret['content-type'] = content_type

        return ret

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
        source_node = validated_data.pop('node', None)

        # Get the Author
        author = get_author(author_data.get('uuid'), author_data.get('node'))

        # Create the post
        post = Post.objects.create(author=author, **validated_data)

        # Append source
        if source_node is not None:
            post.source = source_node.host
            post.save()

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
        source_node = validated_data.pop('node', None)

        # Only update the post if it is timestamped as newer than ours
        pubDate = validated_data.get('pubDate', None)
        if pubDate > instance.pubDate:
            # Call Super to update the Post instance
            instance = super(PostSerializer, self).update(instance, validated_data)
            # Add the categories
            for category in categories_data:
                if category not in instance.categories:
                    instance.categories.add(category)

            # Append source
            if source_node is not None:
                instance.source = source_node.host
                instance.save()

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
