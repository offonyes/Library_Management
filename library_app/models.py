from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from library_app.choice import BorrowStatus, ReservationStatus


class Genre(models.Model):
    name = models.CharField(verbose_name=_('Genre Name'), max_length=100, null=False, blank=False,
                            unique=True)
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name

    def get_books(self):
        return self.books.all()


class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Author Name'),
                            unique=True)
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.name

    def get_books(self):
        return self.books.all()


def current_year():
    return timezone.now().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Book(models.Model):
    authors = models.ManyToManyField(Author, related_name="books", verbose_name=_('Authors'))
    genres = models.ManyToManyField(Genre, related_name="books", verbose_name=_('Genres'),
                                    blank=True)
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Book Title'))
    published_year = models.IntegerField(validators=[MinValueValidator(1800), max_value_current_year],
                                         null=False, blank=False, verbose_name=_('Published Year'))
    stock = models.PositiveIntegerField(default=0, verbose_name=_('Stock'), help_text=_('Number of books'))
    image_link = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Image Link'))

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title


class BookReservation(models.Model):
    book = models.ForeignKey(Book, related_name="reservations", verbose_name=_('Book'), on_delete=models.CASCADE)
    borrower = models.ForeignKey('accounts_app.CustomUser', related_name="reservations", verbose_name=_('Borrower'),
                                 on_delete=models.CASCADE)
    reserved_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Reserved Date'),
                                         help_text=_('Creates automatically'))
    expiration_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Expiration Date'),
                                           help_text=_('Date/time when reservation expires'))
    reservation_status = models.IntegerField(choices=ReservationStatus, default=ReservationStatus.RESERVED,
                                             verbose_name=_('Reservation Status'))

    class Meta:
        verbose_name = _("Book Reservation")
        verbose_name_plural = _("Book Reservations")
        ordering = ['-reserved_date']

    def save(self, *args, **kwargs):
        if not self.expiration_date and self.reservation_status == ReservationStatus.RESERVED:
            self.expiration_date = timezone.now() + timezone.timedelta(days=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} - {self.borrower.email} | {self.reserved_date}"

    @transaction.atomic
    def process_pickup(self):
        if self.reservation_status == ReservationStatus.RESERVED:
            self.reservation_status = ReservationStatus.PICKED_UP
            self.save()

            borrow = BooksBorrow.objects.create(
                book=self.book,
                borrower=self.borrower,
                borrowed_status=BorrowStatus.BORROWED
            )

            self.borrow = borrow
            self.save()


class BooksBorrow(models.Model):
    book = models.ForeignKey(Book, related_name="borrows", verbose_name=_('Book'), on_delete=models.CASCADE)
    borrower = models.ForeignKey('accounts_app.CustomUser', related_name="borrows", verbose_name=_('Borrower'),
                                 on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Borrowed Date'),
                                         help_text=_('Creates automatically'))
    borrowed_status = models.IntegerField(choices=BorrowStatus, default=BorrowStatus.BORROWED,
                                          verbose_name=_('Borrowed Status'))
    return_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Return Date'),
                                       help_text=_('Date/time of returning borrowed book'))

    class Meta:
        verbose_name = _("Books Borrow")
        verbose_name_plural = _("Books Borrows")
        ordering = ['-borrowed_date']

    def __str__(self):
        return f"{self.book.title} - {self.borrower.email} | {self.borrowed_date}"
