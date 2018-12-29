"""Admin view for Catalog Apps."""
from django.contrib import admin

from catalog.models import Author, Genre, Book, BookInstance


class BookInstanceInline(admin.TabularInline):
    """Displaying BookInstance in Book Line."""

    model = BookInstance
    extra = 0


class BookInLine(admin.TabularInline):
    """Displaying Book in Author Line."""

    model = Book
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    """Class for diplaying Author Object in site admin."""

    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInLine]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Class for displaying Book object in site admin."""

    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """class for displaying BookInstance Object in site admin."""

    list_display = ('book', 'status', 'due_back', 'id', 'borrower')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id'),
        }),
        ('Availability', {
            'fields': ('status', 'borrower', 'due_back'),
        }
        )
    )


admin.site.register(Author, AuthorAdmin)
# admin.site.register(BookInstance)
# admin.site.register(Book)
admin.site.register(Genre)
