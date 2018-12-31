"""Database Model for catalog app."""
import uuid
from datetime import date

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(max_length=200, help_text='Enter a book genre')

    def __str__(self):
        """Representation of Genre Model Object."""
        return self.name


class Language(models.Model):
    """Model representing a Language (English, Japan, etc)."""

    name = models.CharField(max_length=200,
                            help_text='Enter the book language')

    def __str__(self):
        """Representation of Language Model Object."""
        return self.name


class Book(models.Model):
    """Model representing a book but not a spesific instance of book."""

    title = models.CharField(max_length=200)

    # ForeignKey is used because book can only have one author,
    # but author can have multiple books
    # Author as a String rather an object, because it's hasn't been
    # declared in file.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000,
                               help_text='Enter a brief description of book.')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character \
                <a href="https://www.isbn-international.org/content/\
                what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can have multiple associated books.
    # And books can cover many genres.
    # Genre class has been defined.
    genre = models.ManyToManyField(Genre,
                                   help_text='Select genres for this book')

    def __str__(self):
        """Representation of Book Model object."""
        return self.title

    def get_absolute_url(self):
        """Return the url to access detail of this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for Genre.Used to display genre in Site Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a spesific copy of a book."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book\
                                    across whole library.')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book Availability',
    )

    class Meta:
        """Meta class of BookInstance."""

        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"), )

    def __str__(self):
        """Representation of BookInstance Model Object."""
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        """Check is a loaned book is over the due date."""
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """Model representing an author."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        """Display order of Author in Admin Site."""

        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Return an url to access a particular author."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Representation of Author Model Object."""
        return f'{self.last_name}, {self.first_name}'
