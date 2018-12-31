"""Unittest for Database Models in catalog app."""

from django.test import TestCase

from catalog.models import Author


class AuthorTestCase(TestCase):
    """UnitTest for Author Model."""

    @classmethod
    def setUpTestData(cls):
        """Set up non modified object."""
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        """Check the label of first_name field in template."""
        author = Author.objects.get(pk=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_last_name_label(self):
        """Check the label of last_name field in template."""
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_date_of_birth_label(self):
        """Check the label of date_of_birth field in template."""
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'date of birth')

    def test_date_of_death_label(self):
        """Check our defined label on date_of_death field."""
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')

    def test_first_name_max_length(self):
        """Check the max length of first_name field."""
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_last_name_max_length(self):
        """Check the max length of last_name field."""
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        """Check Whether the returned format is 'last_name, first_name'."""
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        """Check the given url to author's profile."""
        author = Author.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')
