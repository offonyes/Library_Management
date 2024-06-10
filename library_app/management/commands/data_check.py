from django.core.management.base import BaseCommand
from library_app.models import Book, BookReservation, BooksBorrow
from accounts_app.models import CustomUser
from django.utils import timezone
import random
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Generates user, reservation, wishlist, borrow for testing check commands'

    def handle(self, *args, **kwargs):
        user = CustomUser.objects.create(
            email='dimitri.katranidis@gmail.com',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            personal_number=fake.unique.random_number(digits=11, fix_len=True),
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=90)
        )
        user.set_password('password123')
        user.save()

        books = list(Book.objects.all())

        reservation = BookReservation.objects.create(
            book=random.choice(books),
            borrower=user,
            reservation_status=1
        )
        BookReservation.objects.filter(id=reservation.id).update(
            reserved_date=timezone.now() - timezone.timedelta(days=10),
            expiration_date=timezone.now() - timezone.timedelta(days=9)
        )

        wishlist = BookReservation.objects.create(
            book=random.choice(books),
            borrower=user,
            reserved_date=timezone.now(),
            reservation_status=4
        )

        borrow = BooksBorrow.objects.create(
            book=random.choice(books),
            borrower=user,
            borrowed_status=1
        )
        BooksBorrow.objects.filter(id=borrow.id).update(
            borrowed_date=timezone.now() - timezone.timedelta(days=40)
        )

        self.stdout.write(self.style.SUCCESS('Successfully generated user for testing check commands.'))
