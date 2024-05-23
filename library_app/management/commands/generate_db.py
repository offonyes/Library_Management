from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from library_app.models import Book, Author, Genre
import csv
import re
import random


class Command(BaseCommand):
    help = 'Generates book, genre and author database'

    def handle(self, *args, **kwargs):
        csv_file = "data.csv"

        with open(csv_file, newline='', encoding='utf-8') as file:
            csvreader = csv.reader(file)

            headers = next(csvreader)
            title_index = headers.index('title')
            authors_index = headers.index('authors')
            genres_index = headers.index('categories')
            thumbnail = headers.index('thumbnail')
            published_date_index = headers.index('published_year')

            for num, row in enumerate(csvreader):
                if num == 1000:
                    break
                title = row[title_index]
                categories = row[genres_index]
                authors = row[authors_index]
                published_date = row[published_date_index]
                image = row[thumbnail]

                genres = []
                author = []
                genres.extend([genre.strip() for genre in re.split('&|amp|;', categories) if genre.strip()])
                author.extend([author.strip() for author in re.split('&|amp|;', authors) if author.strip()])
                book = Book.objects.create(
                    title=title,
                    published_date=published_date,
                    stock=random.randint(1, 15),
                    image_link=image
                )
                for genre in genres:
                    if genre == 'none':
                        continue
                    genre_obj = Genre.objects.get_or_create(name=genre)
                    book.genres.add(genre_obj)
                for autho in author:
                    if autho == 'none':
                        continue
                    autho_obj = Author.objects.get_or_create(name=autho)
                    book.authors.add(autho_obj)

        self.stdout.write("Done")
