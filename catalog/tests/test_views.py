"""Unittest for all views in catalog app."""

from django.test import TestCase
from django.urls import reverse

from catalog.models import Author


class AuthorListViewTest(TestCase):
    """Test `AuthorListView`."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exist_at_desired_location(self):
        """Test whether view exists at determined url."""
        response = self.client.get('/catalog/authors')
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test Whether view is accessible by url name."""
        response = self.client.get(reverse('authors'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test whether view uses correct template."""
        response = self.client.get(reverse('authors'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        """Test whether the pagination is 10."""
        response = self.client.get(reverse('authors'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['author_list']) == 10)

    def test_list_all_authors(self):
        """Test whether the second page has remaining 3 author datas."""
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['author_list']) == 3)
