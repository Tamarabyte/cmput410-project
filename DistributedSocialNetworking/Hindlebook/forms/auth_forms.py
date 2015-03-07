from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from Hindlebook.forms.template_mixin import TemplateMixin

class LoginForm(BaseAuthenticationForm, TemplateMixin):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
 
    error_messages = {
        'invalid_login': "*invalid %(username)s or password.",
        'inactive': "*this account is inactive.",
    }