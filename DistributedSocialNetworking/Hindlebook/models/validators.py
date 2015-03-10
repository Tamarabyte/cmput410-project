from django.core.validators import RegexValidator
import re

class UuidValidator(RegexValidator):

    regex = re.compile('^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')
    message = 'Malformed UUID'
    code = 'invalid'
    inverse_match = False

    def __init__(self, **kwargs):
        super(UuidValidator, self).__init__(**kwargs)

