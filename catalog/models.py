import uuid

from django.db import models
from django.urls import reverse


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre')

    def __str__(self):
        """String representation of Genre Model Object."""
        return self.name


class Language(models.Model):
    """Model representing a Language (English, Japan, etc)."""
    name = models.CharField(max_length=200, help_text='Enter the book language')

    def __str__(self):
        """String for representing a Model Object."""
        return self.name


class Book(models.Model):
    """Model representing a book but not a spesific instance of book."""
    title = models.CharField(max_length=200)

    # ForeignKey is used because book can only have one author, but author can have multiple books
    # Author as a String rather an object, becase it's hasn't been declared yet in file.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of book.')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character \
                            <a href="https://www.isbn-international.org/content/what-isbn">\
                            ISBN number</a>')

    # ManyToManyField used because genre can have multiple associated books.
    # And books can cover many genres.
    # Genre class has been defined.
    genre = models.ManyToManyField(Genre, help_text='Select genres for this book')

    def __str__(self):
        """ String for representing Book Model object."""
        return self.title

    def get_absolute_url(self):
        """Return the url to access detail of this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for Genre. Required to display genre in Site Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a spesific copy of a book (i.e. that can be borrowed from the library."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library.')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS=(
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
        ordering = ['due_back']


    def __str__(self):
        """String for representing the Model Object"""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Death', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Return an url to access a particular author."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model Object."""
        return f'{self.last_name}, {self.first_name}'
