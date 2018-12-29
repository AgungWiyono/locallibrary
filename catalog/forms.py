"""Forms class for catalog app."""

from django import forms

class RenewBooks(forms.Form):
    renewal_date = forms.DateField(help_text='Enter a date between now and 4 weeks.')
