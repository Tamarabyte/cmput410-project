from django import forms
from Hindlebook.models import User
from Hindlebook.forms.template_mixin import TemplateMixin


class ProfileEditForm(forms.ModelForm, TemplateMixin):
    """Form for editing user profile"""
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)


    class Meta:
        model = User
        fields = ['about', 'github_id', 'avatar']

class FriendRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FriendRequestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['follows', 'uuid']
        # exclude = ('username', 'password', 'uuid')
