"""Url for catalog app."""
from django.urls import path, include

from catalog import views

author_url = [
    path('authors', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(),
         name='author-detail'),
    path('author/create/', views.AuthorCreate.as_view(),
         name='author_create'),
    path('author/<int:pk>/update', views.AuthorUpdate.as_view(),
         name='author_update'),
    path('author/<int:pk>/delete', views.AuthorDelete.as_view(),
         name='author_delete'),
]

book_url = [
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create/', views.BookCreate.as_view(), name='author_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(),
         name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(),
         name='book_delete'),
]

main_url = [
    path('', views.index, name='index'),
    path('mybooks/', views.LoanedBookByUserListView.as_view(),
         name='my-borrowed'),
    path('borrowed/', views.LibrarianCheckBorrowedBook.as_view(),
         name='borrowed-list'),
    path('book/<uuid:pk>/renew/', views.librarian_renew_book,
         name='librarian-renew-book'),
]

urlpatterns = main_url\
        + author_url\
        + book_url
