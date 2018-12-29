from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404

# Create your views here.

from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    """View function for homepage site."""

    # Number of Book and BookInstance
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()

    # Available Books
    num_instance_available = BookInstance.objects.filter(status__exact='a').count()

    # Number of Author
    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instance,
        'num_instances_available': num_instance_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    """Generic class for displaying all books."""
    model = Book
    context_method_name = 'book_list'
    queryset = Book.objects.all()
    paginate_by = 10
    template_name = 'book_view_all.html'


class BookDetailView(generic.DetailView):
    """Generic class for diplaying a Book."""
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
    """Generic class for displaying all Authors."""
    model = Author
    context_method_name = 'author_list'
    queryset = Author.objects.all()
    paginate_by = 10
    template_name = 'author_view_all.html'


class AuthorDetailView(generic.DetailView):
    """Generic class for displaying an Author."""
    model = Author
    template_name = 'author_detail.html'
