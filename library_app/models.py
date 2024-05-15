from django.db import models
from django.utils.translation import gettext_lazy as _

from library_app.choice import STATUS_TYPE

# Create your models here.


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


class Book(models.Model):
    authors = models.ManyToManyField(Author, related_name="books", verbose_name=_('Authors'))
    genres = models.ManyToManyField(Genre, related_name="books", verbose_name=_('Genres'))
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Book Title'))
    published_date = models.DateField(null=False, blank=False, verbose_name=_('Published Date'))
    stock = models.PositiveIntegerField(default=0, verbose_name=_('Stock'), help_text=_('Number of books'))
    # borrowed_books = models.PositiveIntegerField(default=0, verbose_name=_('Borrowed Books'),
    #                                              help_text=_('Number of borrowed books'))

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ['title', 'published_date']

    def __str__(self):
        return self.title

    def borrowed_books(self):
        return self.borrows.filter(borrowed_status='borrowed').count()

    def reservation_books(self):
        return self.borrows.filter(borrowed_status='pending').count()


class BooksBorrow(models.Model):
    book = models.ForeignKey(Book, related_name="borrows", verbose_name=_('Book'), on_delete=models.CASCADE)
    borrower = models.ForeignKey('accounts_app.CustomUser', related_name="borrows", verbose_name=_('Borrower'),
                                 on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Borrowed Date'),
                                         help_text=_('Creates automatically'))
    borrowed_status = models.CharField(max_length=10, choices=STATUS_TYPE, default='pending',
                                       verbose_name=_('Borrowed Status'))
    return_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Return Date'),
                                       help_text=_('Date/time of returning borrowed book'))

    class Meta:
        verbose_name = _("Books Borrow")
        verbose_name_plural = _("Books Borrows")
        ordering = ['-borrowed_date']

    def __str__(self):
        return f"{self.book.title} - {self.borrower.email} | {self.borrowed_date}"
