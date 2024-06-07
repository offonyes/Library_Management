from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail

from library_app.models import BookReservation
from library_app.choice import ReservationStatus, BorrowStatus


class Command(BaseCommand):
    help = 'Checks the wishlist books and sends email notifications when they are ready for reservation.'

    def handle(self, *args, **kwargs):
        wishlists = BookReservation.objects.filter(
            reservation_status=ReservationStatus.WISHLIST,
        )

        for wishlist in wishlists:
            book = wishlist.book
            borrowed_count = (book.borrows.filter(borrowed_status__in=[BorrowStatus.BORROWED, BorrowStatus.OVERDUE])
                              .count())
            reserved_count = book.reservations.filter(reservation_status=ReservationStatus.RESERVED).count()
            if (borrowed_count + reserved_count) < book.stock:
                subject = 'Your wishlist book is ready for reservation.'
                message = (f'Dear {wishlist.borrower.first_name} {wishlist.borrower.last_name},'
                           f'\n\nYour wishlist for book {wishlist.book.title} is now ready for reservation. '
                           f'Please do it as soon as possible.')
                recipient_list = [wishlist.borrower.email]

                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        if not wishlists.exists():
            self.stdout.write(self.style.SUCCESS('The person to whom to send the message was not found.'))
