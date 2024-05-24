from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django_admin_inline_paginator.admin import TabularInlinePaginated

from library_app.forms import BookReservationForm, BooksBorrowForm
from library_app.models import Book, Author, Genre, BooksBorrow, BookReservation
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
    verbose_name = _('Book Borrowing History')
    verbose_name_plural = _('Book Borrowing Histories')
    can_delete = False
    per_page = 10
    max_num = 0
    readonly_fields = ['book', 'borrower', 'borrowed_status', 'return_date']

    def get_queryset(self, request):
        return super(BooksInline, self).get_queryset(request).select_related(
            'book', 'borrower')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BooksInline]
    list_display = ['title', 'published_date', 'stock', 'borrowed_books', 'reservation_books', 'borrowed_count']
    readonly_fields = ['borrowed_books', 'reservation_books', 'borrowed_count']
    autocomplete_fields = ['authors', 'genres']
    list_filter = [AuthorsFilter, GenresFilter]
    list_per_page = 25
    search_fields = ['title']
    fieldsets = (
        ("Book Information", {'fields': (('title', 'published_date'), ('authors', 'genres'), 'image_link', 'stock'),
                              'classes': ('extra',)}),
        ("Book Stats", {'fields': (('reservation_books', 'borrowed_books'), 'borrowed_count'),
                        "classes": ("wide",)})

    )

    def get_queryset(self, request):
        qs = super(BookAdmin, self).get_queryset(request).prefetch_related('genres', 'authors')

        qs = qs.annotate(
            borrowed_books=Count('borrows', filter=Q(
                borrows__borrowed_status__in=['borrowed', 'overdue']), distinct=True),
            borrowed_count=Count('borrows', filter=Q(
                borrows__borrowed_status__in=['borrowed', 'returned', 'overdue', 'overdue_returned']), distinct=True),
            reservation_books=Count('reservations', filter=Q(
                reservations__reservation_status='reserved'), distinct=True),
        ).order_by('-borrowed_count', '-reservation_books')

        return qs

    def borrowed_books(self, obj):
        return obj.borrowed_books

    borrowed_books.short_description = 'Now Borrowed Books'

    def reservation_books(self, obj):
        return obj.reservation_books

    reservation_books.short_description = 'Reservation Books'

    def borrowed_count(self, obj):
        return obj.borrowed_count

    borrowed_count.short_description = 'Borrowed Books Counts'


@admin.register(BookReservation)
class BookReservationAdmin(admin.ModelAdmin):
    form = BookReservationForm
    list_display = ['id', 'book', 'borrower', 'reserved_date', 'reservation_status']
    fieldsets = [
        ('Information', {
            'fields': (('book', 'borrower'), 'reserved_date', 'expiration_date'),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('reservation_status',)
        })
    ]
    list_filter = [BooksFilter, BorrowersFilter, ('reserved_date', DateFieldListFilter), 'reservation_status']
    readonly_fields = ['reserved_date', 'expiration_date']
    autocomplete_fields = ['book', 'borrower']
    actions = ['mark_as_picked_up']

    def mark_as_picked_up(self, request, queryset):
        for reservation in queryset:
            if reservation.reservation_status == 'reserved':
                reservation.process_pickup()
        self.message_user(request, "Selected reservations have been marked as picked up and borrow records created.")

    mark_as_picked_up.short_description = "Mark selected reservations as picked up"

    def save_model(self, request, obj, form, change):
        if change:
            previous_status = BookReservation.objects.get(pk=obj.pk).reservation_status
            if previous_status != 'picked_up' and obj.reservation_status == 'picked_up':
                BooksBorrow.objects.create(
                    book=obj.book,
                    borrower=obj.borrower,
                    borrowed_status='borrowed'
                )
                self.message_user(request, "Selected reservation have been marked as picked"
                                           " up and borrow records created.")

        super().save_model(request, obj, form, change)


@admin.register(BooksBorrow)
class BooksBorrowAdmin(admin.ModelAdmin):
    form = BooksBorrowForm
    list_display = ['id', 'book', 'borrower', 'borrowed_date', 'borrowed_status', 'return_date']
    fieldsets = (
        ('Information', {'fields': (('book', 'borrower'), 'borrowed_date'),
                         'classes': ('wide',)}),
        ('Status', {'fields': ('borrowed_status',)}),
        ('Return', {'fields': ('return_date',),
                    'classes': ('collapse',)})

    )
    list_filter = [BooksFilter, BorrowersFilter, ('borrowed_date', DateFieldListFilter), 'borrowed_status']
    readonly_fields = ['borrowed_date']
    autocomplete_fields = ['book', 'borrower']

    def get_queryset(self, request):
        return super(BooksBorrowAdmin, self).get_queryset(request).select_related(
            'book', 'borrower')

    def save_model(self, request, obj, form, change):
        if obj.borrowed_status in ['returned', 'overdue_returned']:
            obj.return_date = timezone.now()
        super().save_model(request, obj, form, change)
