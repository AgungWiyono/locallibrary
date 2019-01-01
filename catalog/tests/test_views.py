"""Unittest for all views in catalog app."""

import datetime
import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Permission

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
        self.assertEqual(response.status_code, 200)

        # Check that we don't have any book loaned
        self.assertTrue('bookinstancelist' in response.context)
        self.assertEqual(len(response.context['bookinstancelist']), 0)

        # Change some books's status to loan('o')
        books = BookInstance.objects.all()[:10]
        for book in books:
            book.status = 'o'
            book.save()

        # Repeat the login proccess
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        # Check borrowed book list in page
        self.assertTrue('bookinstancelist' in response.context)

        # Confirm all book belong to testuser1
        for book in response.context['bookinstancelist']:
            self.assertEqual(response.context['user'], book.borrower)
            self.assertEqual('o', book.status)

    def test_booklist_ordered_by_due_date(self):
        """Test that booklist should be ordered by due date."""
        # Change all book's status to loan('o')
        for book in BookInstance.objects.all():
            book.status = 'o'
            book.save()

        # Login into page
        login = self.client.login(
                                username='testuser1',
                                password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check that user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        # Confirm that only 10 items are displayed per page
        self.assertEqual(len(response.context['bookinstancelist']), 10)

        last_date = 0
        for book in response.context['bookinstancelist']:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back


class LibrarianRenewBookViewTest(TestCase):
    """Test LibrarianRenewBook View."""

    def setUp(self):
        """Create data for testing."""
        # Create user
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

        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(
                                        first_name='John',
                                        last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_book = Book.objects.create(
                title='Book Title',
                summary='My book summary',
                isbn='ABCDEFG',
                author=test_author,
        )

        # Assign a genre to book
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
                        book=test_book,
                        imprint='Unlikely Imprint, 2016',
                        due_back=return_date,
                        borrower=test_user1,
                        status='o',
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
                        book=test_book,
                        imprint='Unlikely Imprint, 2016',
                        due_back=return_date,
                        borrower=test_user2,
                        status='o',
        )

    def test_redirect_if_not_logged_in(self):
        """Unlogged in user should be redirected."""
        response = self.client.get(
                            reverse('librarian-renew-book',
                                    kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_wrong_permission(self):
        """Logged in user who doesn't have permission should be redirected."""
        login = self.client.login(username='testuser1',
                                  password='1X<ISRUkw+tuK')
        response = self.client.get(
                        reverse('librarian-renew-book',
                                kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_permission_borrowed_book(self):
        """Logged in user with permission should be able to access page."""
        login = self.client.login(
                            username='testuser2',
                            password='2HJ1vRV0Z&3iD')
        response = self.client.get(
                        reverse('librarian-renew-book',
                                kwargs={'pk': self.test_bookinstance2.pk}))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_permission_another_user_borrowed_book(self):
        """Librarian should be able to renew all borrowed book."""
        login = self.client.login(
                            username='testuser2',
                            password='2HJ1vRV0Z&3iD')
        response = self.client.get(
                            reverse('librarian-renew-book',
                                    kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_invalid_book_logged_in(self):
        """Return http404 if no book with given uid exists."""
        test_uid = uuid.uuid4()
        login = self.client.login(
                            username='testuser2',
                            password='2HJ1vRV0Z&3iD')
        response = self.client.get(
                            reverse('librarian-renew-book',
                                    kwargs={'pk': test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        """Correct template should be used."""
        login = self.client.login(
                            username='testuser2',
                            password='2HJ1vRV0Z&3iD')
        response = self.client.get(
                            reverse('librarian-renew-book',
                                    kwargs={'pk': self.test_bookinstance2.pk}))
        self.assertTemplateUsed('catalog/librarian_renew_book.html')

    def test_due_back_field_initial_value(self):
        """Initial value for 'due_back' field should be 3 weeks ahead."""
        login = self.client.login(
                            username='testuser2',
                            password='2HJ1vRV0Z&3iD')
        response = self.client.get(
                            reverse('librarian-renew-book',
                                    kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        future_3_weeks = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['due_back'],
                         future_3_weeks)

    def test_redirect_on_all_borrowed_book(self):
        """After successed renewing, should redirect to 'borrowed/'."""
        login = self.client.login(
                            username='testuser2',
                            password='2HJ1vRV0Z&3iD')

        # Valid date for book renewal
        valid_date = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(
                        reverse('librarian-renew-book',
                                kwargs={'pk': self.test_bookinstance1.pk}),
                        {'due_back': valid_date})
        self.assertRedirects(response, reverse('borrowed-list'))

    def test_form_invalid_date_in_past(self):
        """Form invalid for due_back in the past."""
        login = self.client.login(
                            username='testuser2',
                            password='2HJ1vRV0Z&3iD')
        past_date = datetime.date.today() - datetime.timedelta(days=1)
        response = self.client.post(
                        reverse('librarian-renew-book',
                                kwargs={'pk': self.test_bookinstance2.pk}),
                        {'due_back': past_date})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response,
                             'form',
                             'due_back',
                             'Invalid date - renewal in the past')

    def test_form_invalid_date_more_4_weeks(self):
        """For invalid for due_back more than 4 weekse ahead."""
        login = self.client.login(
                            username='testuser2',
                            password='2HJ1vRV0Z&3iD')
        future_date = datetime.date.today()\
                     + datetime.timedelta(weeks=4, days=1)
        response = self.client.post(
                        reverse('librarian-renew-book',
                                kwargs={'pk': self.test_bookinstance1.pk}),
                        {'due_back': future_date})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response,
                             'form',
                             'due_back',
                             'Invalid date - renewal more than 4 weeks a ahead')
