from django.core.management.base import BaseCommand
from django.utils import timezone
from library_app.models import BookReservation


class Command(BaseCommand):
    help = 'Checks whether the reservation time has expired.'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_reservations = BookReservation.objects.filter(
            reservation_status='reserved',
            expiration_date__lt=now
        )

        for reservation in expired_reservations:
            reservation.reservation_status = 'reservation_expired'
            reservation.save()

        if not expired_reservations.exists():
            self.stdout.write(self.style.SUCCESS('No expired reservations found.'))
