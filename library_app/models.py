from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Genre(models.Model):
    name = models.CharField(verbose_name=_('Genre Name'), max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self


class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Author Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Book Title'))
    authors = models.ManyToManyField(Author, related_name="books", verbose_name=_('Authors'))
    genres = models.ManyToManyField(Genre, related_name="books", verbose_name=_('Genres'))
    published_date = models.DateField(null=False, blank=False, verbose_name=_('Published Date'))
    stock = models.PositiveIntegerField(default=0, verbose_name=_('Stock'))

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ['title', 'published_date']

    def __str__(self):
        return self.title
