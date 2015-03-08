from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm, CharField, ValidationError, PasswordInput
from Hindlebook.forms.template_mixin import TemplateMixin
User = get_user_model()

class LoginForm(BaseAuthenticationForm, TemplateMixin):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
 
    error_messages = {
        'invalid_login': "Invalid %(username)s or password.",
        'inactive': "This account is waiting for admin activation.",
    }
    
class RegistrationForm(ModelForm, TemplateMixin):
    """
    Form for registering a new user account.
    Validates that the requested username and email is not already in use, and
    requires the password to be entered twice to catch typos.
    """
    
    error_messages = {
        'duplicate_username': "User already exists",
        'duplicate_email' : "This email already in use",
        'password_mismatch': "Passwords fields don't match",
    }

    password1 = CharField(widget=PasswordInput, label="Password")
    password2 = CharField(widget=PasswordInput, label="Password (again)")

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username' : 'Letters, digits and @/./+/_ only.',
            'email' : "Not required, but we'll send you an email when your registration is approved",
        }
    
    def clean_username(self):
        """
        Validate that the username is not already in use.
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__iexact=username):
            raise ValidationError(self.error_messages['duplicate_username'])
        
        return username
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the site.
        """
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email):
            raise ValidationError(self.error_messages['duplicate_email'])
        return email
    
    def clean_password2(self):
        """
        Verifiy that the values entered into the two password fields match.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'])
        
        return password2
    
    def save(self, commit=True):
        """ Save the provided password in a hashed format.
        """
        # Save the provided password in hashed format
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        
        if commit:
            user.save()

        return user
