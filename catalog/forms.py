"""Forms class for catalog app."""

import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from catalog.models import BookInstance


class RenewBookForm(forms.ModelForm):
    """Form for updating due back date of borrowed book."""

    def clean_due_back(self):
        """Validate form data."""
        data = self.cleaned_data['due_back']

        # Check if a date is in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in the pas'))

        if data > (datetime.date.today() + datetime.timedelta(weeks=4)):
            raise ValidationError(_('Invalid date -\
                                    renewal more than 4 weeks a ahead'))
        return data

    class Meta:
        """Adjust how the form is displayed."""

        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('New Renewal Date')}
        help_texts = {
            'due_back': _('Enter a date between now and 4 weeks (default 3)')}
