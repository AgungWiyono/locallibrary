"""Unittest for all views in catalog app."""

import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from catalog.models import Author, Book, BookInstance, Genre


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
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test Whether view is accessible by url name."""
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test whether view uses correct template."""
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        """Test whether the pagination is 10."""
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
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


class LoanedBookByUserListViewTest(TestCase):
    """Test for LoanedBookByUserListView."""

    def setUp(self):
        """Create dummy record on database for testing."""
        # Create 2 users
        test_user1 = User.objects.create_user(
                                            username='testuser1',
                                            password='1X<ISRUkw+tuK'
                                            )
        test_user2 = User.objects.create_user(
                                            username='testuser2',
                                            password='2HJ1vRV0Z&3iD'
                                            )

        test_user1.save()
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(first_name='John',
                                            last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_book = Book.objects.create(
            title='Book Title',
            summary='The book summary',
            isbn='ABCDEFG',
            author=test_author,
        )

        # Assign a genre to a book
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()

        # Create 30 exemplars from the book
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.now()\
                    + datetime.timedelta(days=book_copy % 5)
            the_borrower = test_user1 if book_copy % 2 == 0 else test_user2
            status = 'm'
            BookInstance.objects.create(
                book=test_book,
                imprint='Unlikely imprint, 2016',
                due_back=return_date,
                borrower=the_borrower,
                status=status
            )

    def test_redirect_if_not_logged_in(self):
        """
        Should redirect to login if user is not logged in.

        :return: True if anonymous user is redirected, false otherwise
        :rtype: bool
        """
        response = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(
                response,
                '/accounts/login/?next=/catalog/mybooks/'
                )

    def test_logged_in_uses_correct_template(self):
        """
        Test whether the view uses correct template or not.

        :return: True if:
                        - user is logged in
                        - response status is 200
                        - correct template is used
        :rtype: bool
        """
        login = self.client.login(
                                username='testuser1',
                                password='1X<ISRUkw+tuK'
                                )
        response = self.client.get(reverse('my-borrowed'))

        # Check if user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check response status is success(200)
        self.assertEqual(response.status_code, 200)

        # Check view uses correct template
        self.assertTemplateUsed(
                            response,
                            'catalog/loaned_book_by_user.html'
                            )

    def test_only_borrowed_book_in_list(self):
        """
        View should only display the book with status 'o'.

        :return: True if:
                        - user is logged in
                        - response status is 200 after login
                        - return null as no books's status is 'o'
                        - after change books code, display all books with
                          status 'o' and it's borrower
        :rtype: bool
        """
        login = self.client.login(
                                username='testuser1',
                                password='1X<ISRUkw+tuK'
                                )
        response = self.client.get(reverse('my-borrowed'))

        # Check that user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual()
