from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from library_app.models import Book, Author, Genre
import csv
import re
import random


class Command(BaseCommand):
    help = 'Generates book, genre and author database'

    def handle(self, *args, **kwargs):
        csv_file = "google_books_1299.csv"

        with open(csv_file, newline='', encoding='utf-8') as file:
            csvreader = csv.reader(file)

            headers = next(csvreader)
            title_index = headers.index('title')
            authors_index = headers.index('author')
            genres_index = headers.index('generes')
            published_date_index = headers.index('published_date')

            for row in csvreader:
                title = row[title_index]
                categorys = row[genres_index]
                author = row[authors_index]
                published_date = row[published_date_index][-4:]

                genres = []

                genres.extend([genre.strip() for genre in re.split('&|amp|,', categorys) if genre.strip()])
                book = Book.objects.create(
                    title=title,
                    published_date=published_date,
                    stock=random.randint(0, 15),
                )
                for genre in genres:
                    try:
                        genre_obj = Genre.objects.create(name=genre)
                    except IntegrityError as e:
                        genre_obj = Genre.objects.get(name=genre)
                    book.genres.add(genre_obj)
                try:
                    autho_obj = Author.objects.create(name=author)
                except IntegrityError as e:
                    autho_obj = Author.objects.get(name=author)
                book.authors.add(autho_obj)

        self.stdout.write("Done")
