import uuid
from django import forms
from Hindlebook.models.post_models import Post, Comment


class PostForm(forms.ModelForm):
    
    def __init__(self,  *args, **kwargs):
        self.guid = uuid.uuid4
        super(PostForm, self).__init__(*args, **kwargs)

    # pass in a UUID when saving for setting UUIDs from put requests
    def save(self, author, postGUID, commit=False):
        """ Save the provided password in a hashed format.
        """
        # Save the provided password in hashed format
        post = super(PostForm, self).save(commit=False)
        post.author = author
        post.guid = postGUID

        if commit:
            post.save()
    
        return post

    class Meta:
        model = Post
        fields = ['content', 'visibility']

class CommentForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        self.guid = uuid.uuid4
        super(CommentForm, self).__init__(*args, **kwargs)

    # pass in a UUID when saving for setting UUIDs from put requests
    def save(self, author, post, commentGUID, commit=False):
        """ Save the provided password in a hashed format.
        """
        # Save the provided password in hashed format
        comment = super(CommentForm, self).save(commit=False)
        comment.guid = commentGUID
        comment.post = post
        comment.author = author

        if commit:
            comment.save()

        return comment


    class Meta:
        model = Comment
        fields = ['comment']
