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
    def save(self, user, postUUID, commit=True):
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

class CommentForm(forms.ModelForm, TemplateMixin):

    def __init__(self,  *args, **kwargs):
        self.uuid = uuid.uuid4
        super(CommentForm, self).__init__(*args, **kwargs)

    # pass in a UUID when saving for setting UUIDs from put requests
    def save(self, user, postUUID, commit=True):
        """ Save the provided password in a hashed format.
        """
        # Save the provided password in hashed format
        comment = super(CommentForm, self).save(commit=False)


    class Meta:
        model = Comment
        fields = ['text']


"""
class CommentForm(forms.ModelForm, TemplateMixin):


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.post_UUID = kwargs.pop('post_UUID', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    def set_postUUID(self, post_uuid):
        self.post_UUID = post_UUID
        

    def on_valid(self, user):
        p = Post.objects.get(uuid=self.cleaned_data['post_uuid'])
        if p != None:
            new_f = Comment(author=user, text=self.cleaned_data['text'], pub_date=datetime.now(), post=p)
            new_f.save()

    def clean(self):
        cleaned_data = self.cleaned_data
        post_id_key = 'post_uuid'
        if self.post_UUID != None:
            post = str(uuid.UUID(self.post_UUID))
            cleaned_data[post_id_key] = post
        else:
            raise ValidationError("%s key is not in form" %(post_id_key))

        return cleaned_data
"""
