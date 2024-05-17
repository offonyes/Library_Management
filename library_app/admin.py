from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django_admin_inline_paginator.admin import TabularInlinePaginated

from library_app.models import Book, Author, Genre, BooksBorrow
from library_app.filters import AuthorsFilter, GenresFilter, BooksFilter, BorrowersFilter


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


class BooksInline(TabularInlinePaginated):
    model = BooksBorrow
    verbose_name = _('Book History')
    verbose_name_plural = _('Book Histories')
    per_page = 10
    extra = 0
    autocomplete_fields = ['book', 'borrower']
    fieldsets = (
        ('Information', {'fields': (('book', 'borrower'),),
                         'classes': ('wide',)}),
        ('Status', {'fields': ('borrowed_status',)}),
        ('Return', {'fields': ('return_date',)})
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BooksInline]
    list_display = ['title', 'published_date', 'stock', 'borrowed_books', 'reservation_books', 'borrowed_count']
    readonly_fields = ['borrowed_books', 'reservation_books', 'borrowed_count']
    autocomplete_fields = ['authors', 'genres']
    list_filter = [AuthorsFilter, GenresFilter]
    list_per_page = 25
    search_fields = ['title', 'authors__name', 'genres__name']
    fieldsets = (
        ("Book Information", {'fields': (('title', 'published_date'), ('authors', 'genres'), 'stock'),
                              'classes': ('extra',)}),
        ("Book Stats", {'fields': (('reservation_books', 'borrowed_books'), 'borrowed_count'),
                        "classes": ("wide",)})

    )

    def get_queryset(self, request):
        qs = super(BookAdmin, self).get_queryset(request).prefetch_related("genres")
        qs = qs.annotate(
            borrowed_books=Count('borrows', filter=Q(borrows__borrowed_status='borrowed')),
            reservation_books=Count('borrows', filter=Q(borrows__borrowed_status='reserved')),
            borrowed_count=Count('borrows',
                                 filter=Q(borrows__borrowed_status='returned') | Q(borrows__borrowed_status='borrowed'))
        )
        return qs.order_by('-borrowed_count')

    def borrowed_books(self, obj):
        return obj.borrowed_books

    borrowed_books.short_description = 'Now Borrowed Books'

    def reservation_books(self, obj):
        return obj.reservation_books

    reservation_books.short_description = 'Reservation Books'

    def borrowed_count(self, obj):
        return obj.borrowed_count

    borrowed_count.short_description = 'Borrowed Books Counts'


@admin.register(BooksBorrow)
class BooksBorrowAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower', 'borrowed_date', 'borrowed_status', 'return_date']
    fieldsets = (
        ('Information', {'fields': (('book', 'borrower'), 'borrowed_date'),
                         'classes': ('wide',)}),
        ('Status', {'fields': ('borrowed_status',)}),
        ('Return', {'fields': ('return_date',),
                    'classes': ('collapse',)})

    )
    list_filter = [BooksFilter, BorrowersFilter, ('borrowed_date', DateFieldListFilter)]
    readonly_fields = ['borrowed_date']
    autocomplete_fields = ['book', 'borrower']
    # prefetch_related = ('book', 'borrower')

    def save_model(self, request, obj, form, change):
        if obj.borrowed_status == 'returned':
            obj.return_date = timezone.now()
        super().save_model(request, obj, form, change)
