"""Views for catalog apps."""

import datetime


from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm


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

    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
    """Generic class for displaying all books."""

    model = Book
    context_method_name = 'book_list'
    queryset = Book.objects.all()
    paginate_by = 10
    template_name = 'catalog/book_list.html'


class BookDetailView(generic.DetailView):
    """Generic class for diplaying a Book."""

    model = Book
    template_name = 'catalog/book_detail.html'


class AuthorListView(generic.ListView):
    """Generic class for displaying all Authors."""

    model = Author
    context_method_name = 'author_list'
    queryset = Author.objects.all()
    paginate_by = 10
    template_name = 'catalog/author_list.html'


class AuthorDetailView(generic.DetailView):
    """Generic class for displaying an Author."""

    model = Author
    template_name = 'catalog/author_detail.html'


class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic view to see all books on loan to user."""

    model = BookInstance
    template_name = "catalog/loaned_book_by_user.html"
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
    template_name = 'catalog/loaned_book_by_user.html'
    permission_required = 'catalog.can_mark_returned'
    context_object_name = 'bookinstancelist'

    def get_queryset(self):
        """Get all loaned book."""
        return BookInstance.objects.all().filter(
            status__exact='o').order_by(
                'due_back')


@permission_required('catalog.can_mark_returned')
def librarian_renew_book(request, pk):
    """View for renewing borrowed book due back."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            return HttpResponseRedirect(reverse('borrowed-list'))

    else:
        proposed_renewal_date = datetime.date.today()\
                + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={
            'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'librarian_renew_book.html', context=context)


class AuthorCreate(CreateView):
    """Generic view for creating new Author."""

    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(UpdateView):
    """Generic view for updating an Author data."""

    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    """Generic view for deleting an Author data."""

    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    """Generic view for creating new Book."""

    model = Book
    fields = '__all__'


class BookUpdate(UpdateView):
    """Generic view for updating a Book data."""

    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']


class BookDelete(DeleteView):
    """Generic view for deleting a Book."""

    model = Book
    success_url = reverse_lazy('books')
