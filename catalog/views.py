"""Views for catalog apps."""
from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

from catalog.models import Book, Author, BookInstance, Genre


def index(request):
    """View function for homepage site."""
    # Number of Book and BookInstance
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()

    # Available Books
    num_instance_available = BookInstance.objects.filter(
                                status__exact='a').count()

    # Number of Author
    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Number of visit to this page, as counted in session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instance,
        'num_instances_available': num_instance_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    """Generic class for displaying all books."""

    model = Book
    context_method_name = 'book_list'
    queryset = Book.objects.all()
    paginate_by = 10
    template_name = 'book_list.html'


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
    template_name = 'author_list.html'


class AuthorDetailView(generic.DetailView):
    """Generic class for displaying an Author."""

    model = Author
    template_name = 'author_detail.html'


class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic view to see all books on loan to user."""

    model = BookInstance
    template_name = "loaned_book_by_user.html"
    paginate_by = 10
    context_object_name = 'bookinstancelist'

    def get_queryset(self):
        """Get only the loaned book by logged in user."""
        return BookInstance.objects.filter(
            borrower=self.request.user).filter(
            status__exact='o').order_by('due_back')


class LibrarianCheckBorrowedBook(PermissionRequiredMixin, generic.ListView):
    """Generic view for librarian to see all borrowed books."""

    model = BookInstance
    template_name = 'loaned_book_by_user.html'
    permission_required = 'catalog.can_mark_returned'
    context_object_name = 'bookinstancelist'

    def get_queryset(self):
        """Get all loaned book."""
        return BookInstance.objects.all().filter(
            status__exact='o')
