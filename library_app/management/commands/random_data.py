from django.core.management.base import BaseCommand
from library_app.models import Book, BookReservation, BooksBorrow
from accounts_app.models import CustomUser
from django.utils import timezone
import random
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Generates users, reservations and borrows'

    def handle(self, *args, **kwargs):
        self.create_users(10)
        self.create_reservations_and_borrows(100, 100)
        self.stdout.write(self.style.SUCCESS('Successfully generated users, reservations, and borrows.'))

    def create_users(self, count):
        users = []
        for _ in range(count):
            user = CustomUser(
                email=fake.unique.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                personal_number=fake.unique.random_number(digits=11, fix_len=True),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=90)
            )
            user.set_password('password123')
            users.append(user)
        CustomUser.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS(f'Created {count} users.'))

    def create_reservations_and_borrows(self, reservation_count, borrow_count):
        users = list(CustomUser.objects.all())
        books = list(Book.objects.all())

        reservations = []
        borrows = []

        for _ in range(reservation_count):
            reservation = BookReservation(
                book=random.choice(books),
                borrower=random.choice(users),
                reserved_date=timezone.now(),
                expiration_date=timezone.now() + timezone.timedelta(days=1),
                reservation_status=random.randint(1, 5)
            )
            reservations.append(reservation)

        BookReservation.objects.bulk_create(reservations)
        self.stdout.write(self.style.SUCCESS(f'Created {reservation_count} reservations.'))

        for _ in range(borrow_count):
            borrow = BooksBorrow(
                book=random.choice(books),
                borrower=random.choice(users),
                borrowed_date=timezone.now(),
                borrowed_status=random.randint(1, 4),
            )
            borrows.append(borrow)

        BooksBorrow.objects.bulk_create(borrows)
        self.stdout.write(self.style.SUCCESS(f'Created {borrow_count} borrows.'))
