from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from library_app.models import BooksBorrow
from library_app.choice import BorrowStatus


class Command(BaseCommand):
    help = 'Checks whether the borrowed books should be marked as overdue and sends email notifications.'

    def handle(self, *args, **kwargs):
        now = timezone.now() - timezone.timedelta(days=14)
        expired_borrows = BooksBorrow.objects.filter(
            borrowed_status=BorrowStatus.BORROWED,
            borrowed_date__lt=now
        )

        for borrow in expired_borrows:
            borrow.borrowed_status = BorrowStatus.OVERDUE

            subject = 'Your borrowed book is overdue'
            message = (f'Dear {borrow.borrower.first_name} {borrow.borrower.last_name},\n\nYour borrowed book'
                       f' "{borrow.book.title}" is now overdue. Please return it as soon as possible.')
            recipient_list = [borrow.borrower.email]

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            borrow.save()

        if not expired_borrows.exists():
            self.stdout.write(self.style.SUCCESS('No expired reservations found.'))
