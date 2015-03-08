from django import forms
from Hindlebook.models import User


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile"""
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['about']
        # exclude = ('username', 'password', 'uuid')
