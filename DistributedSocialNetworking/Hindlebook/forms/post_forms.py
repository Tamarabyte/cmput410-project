import uuid
from django import forms
from Hindlebook.models import Post, Comment, Settings, Category

class MultipleChoiceFieldNoValidation(forms.MultipleChoiceField):
    def validate(self, value):
        pass

class PostForm(forms.ModelForm):

    #(widget=PasswordInput, label="Password")
    def __init__(self, *args, **kwargs):
        self.guid = uuid.uuid4
        super(PostForm, self).__init__(*args, **kwargs)
        
        self.category_choices = [category.tag for category in Category.objects.all()];
        
        # add fields here so we can dynamically set choices on form creations
        self.fields['categories'] = MultipleChoiceFieldNoValidation(choices=zip(self.category_choices, self.category_choices))
    
    def clean_categories(self):
        """
        Validate that the supplied email address is unique for the site.
        """
        tags = self.cleaned_data.get("categories")
        for tag in tags:
            if tag not in self.category_choices:
                Category.objects.get_or_create(tag=tag)
        return tags

    # pass in a UUID when saving for setting UUIDs from put requests
    def save(self, author, postGUID, commit=False):
        """ Save the provided password in a hashed format.
        """
        # Save the provided password in hashed format
        post = super(PostForm, self).save(commit=False)
        post.author = author
        post.guid = postGUID
        post.source = Settings.objects.all().first().node.host
        post.origin = Settings.objects.all().first().node.host
        post.description = post.title
        
        tags = Category.objects.filter(pk__in=self.cleaned_data.get("categories"))
        post.categories.add(*tags)
        if commit:
            post.save()
            self.save_m2m()

        return post
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'visibility', 'content_type']


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
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
