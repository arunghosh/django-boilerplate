from django.utils.translation import ugettext_lazy as _
from django.core import validators


class ValidationInfo:

    def __init__(self, validators, text=''):
        self.validators = validators
        self.help_text = text

mobile =  ValidationInfo([validators.RegexValidator(r'^\d{10}$', _('Enter a valid phone number.'), 'invalid')])

password = ValidationInfo([validators.RegexValidator(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')],
    _('Should have minimum length of 8. Should contain alteast an uppercase alpahabet, a lowecase alpahabet, a number and a special character.'))

# username = ValidationInfo([validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')], 
    # '30 characters or fewer. Letters, digits and ' '@/./+/-/_ only.'
# )

