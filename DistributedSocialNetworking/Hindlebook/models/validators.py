from django.core.validators import RegexValidator
import re

class UuidValidator(RegexValidator):

    regex = re.compile('^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$')
    message = 'Malformed UUID'
    code = 'invalid'
    inverse_match = False

    def __init__(self, **kwargs):
        super(UuidValidator, self).__init__(**kwargs)

