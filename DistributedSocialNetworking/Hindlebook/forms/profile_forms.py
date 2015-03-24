from django import forms
from Hindlebook.forms.template_mixin import TemplateMixin
from Hindlebook.models import Author


class ProfileEditForm(forms.ModelForm, TemplateMixin):
    """Form for editing user profile"""
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Author
        fields = ['about', 'github_id', 'avatar']


class FriendRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FriendRequestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Author
        fields = ['follows', 'uuid']
