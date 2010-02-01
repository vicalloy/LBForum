"""
Forms and validation code for user registration.

"""
from django import forms
from registration.forms import RegistrationFormUniqueEmail

from django.utils.translation import ugettext_lazy as _


attrs_dict = { 'class': 'required' }

class CnRegistrationFormUniqueEmail(RegistrationFormUniqueEmail):
    username = forms.RegexField(regex=r'(?u)^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
