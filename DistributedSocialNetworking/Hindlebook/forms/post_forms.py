import uuid
from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError


from Hindlebook.models.post_models import Post, Comment
from Hindlebook.forms.template_mixin import TemplateMixin

class PostForm(forms.ModelForm, TemplateMixin):
    
    def __init__(self,  *args, **kwargs):
        self.uuid = uuid.uuid4
        super(PostForm, self).__init__(*args, **kwargs)

    # pass in a UUID when saving for setting UUIDs from put requests
    def save(self, user, postUUID, commit=False):
        """ Save the provided password in a hashed format.
        """
        # Save the provided password in hashed format
        post = super(PostForm, self).save(commit=False)
        post.author = user
        post.uuid = postUUID

        # Update this with logic to detect content type
        post.content_type = 0

        if commit:
            post.save()
    
        return post

    class Meta:
        model = Post
        fields = ['text']

class CommentForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        self.uuid = uuid.uuid4
        super(CommentForm, self).__init__(*args, **kwargs)

    # pass in a UUID when saving for setting UUIDs from put requests
    def save(self, user, post, commentUUID, commit=False):
        """ Save the provided password in a hashed format.
        """
        # Save the provided password in hashed format
        comment = super(CommentForm, self).save(commit=False)
        comment.post = post
        comment.author = user

        if commit:
            comment.save()

        return comment


    class Meta:
        model = Comment
        fields = ['text']
        exclude = ["author"]
