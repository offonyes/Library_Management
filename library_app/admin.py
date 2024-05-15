from django.contrib import admin

from library_app.models import Book, Author, Genre, BooksBorrow
from library_app.filters import AuthorsFilter, GenresFilter


# Register your models here.


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_per_page = 10


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_per_page = 10


class BooksInline(admin.StackedInline):
    model = BooksBorrow
    extra = 0
    autocomplete_fields = ['book', 'borrower']
    fieldsets = (
        ('Information', {'fields': (('book', 'borrower'),),
                         'classes': ('wide',)}),
        ('Status', {'fields': ('borrowed_status',)}),
        ('Return', {'fields': ('return_date',),
                    'classes': ('collapse',)})
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BooksInline]
    list_display = ['title', 'published_date', 'stock', 'borrowed_books']
    readonly_fields = ['borrowed_books']
    autocomplete_fields = ['authors', 'genres']
    list_filter = [AuthorsFilter, GenresFilter]
    list_per_page = 25
    search_fields = ['title', 'authors__name', 'genres__name']
    fieldsets = (
        ("Book Information", {'fields': (('title', 'published_date'), ('authors', 'genres'), 'stock'),
                              'classes': ('wide',)}),
        ("Borrowed Books", {'fields': ('borrowed_books',)})

    )

    def get_queryset(self, request):
        qs = super(BookAdmin, self).get_queryset(request)
        qs = qs.prefetch_related('borrows')
        return qs


@admin.register(BooksBorrow)
class BooksBorrowAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower', 'borrowed_date']
    fieldsets = (
        ('Information', {'fields': (('book', 'borrower'), 'borrowed_date'),
                         'classes': ('wide',)}),
        ('Status', {'fields': ('borrowed_status',)}),
        ('Return', {'fields': ('return_date',),
                    'classes': ('collapse',)})

    )
    readonly_fields = ['borrowed_date']
    autocomplete_fields = ['book', 'borrower']
