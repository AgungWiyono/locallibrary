"""Unittest for all form in catalog app."""

import datetime

from django.test import SimpleTestCase
from django.utils import timezone

from catalog.forms import RenewBookForm


class RenewBookFormTest(SimpleTestCase):
    """Unittest for RenewBookForm."""

    def test_date_field_label(self):
        """Check the due_back field label."""
        form = RenewBookForm()
        self.assertTrue(form.fields['due_back'].label is None or
                        form.fields['due_back'].label == 'New Renewal Date')

    def test_date_field_help_text(self):
        """Check `due_back` field helptext."""
        form = RenewBookForm()
        self.assertEquals(form.fields['due_back'].help_text,
                          'Enter a date between now and 4 weeks (default 3)')

    def test_date_in_the_past(self):
        """Form shouldn't be valid for inputted date that in the past."""
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'due_back': date})
        self.assertFalse(form.is_valid())

    def test_date_too_far_in_the_future(self):
        """Form shouldn't be valid for date that is more than 4 weeks."""
        date = datetime.date.today()\
            + datetime.timedelta(weeks=4)\
            + datetime.timedelta(days=1)
        form = RenewBookForm(data={'due_back': date})
        self.assertFalse(form.is_valid())

    def test_date_today(self):
        """Form should be valid for today's date."""
        date = datetime.date.today()
        form = RenewBookForm(data={'due_back': date})
        self.assertTrue(form.is_valid())

    def test_date_max(self):
        """Form should be valid for the date 4 weeks in the future."""
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'due_back': date})
        self.assertTrue(form.is_valid())
