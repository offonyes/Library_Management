from django.utils.translation import gettext_lazy as _
from django.db import models


class BorrowStatus(models.IntegerChoices):
    BORROWED = 1, _('Borrowed a book')  # Borrowed Book
    RETURNED = 2, _('Returned a book')  # Returned in time
    OVERDUE = 3, _('Overdue book')  # 2 weeks passed and didn't return yet
    OVERDUE_RETURNED = 4, _('Returned overdue book')  # Returned after 2 weeks


class ReservationStatus(models.IntegerChoices):
    RESERVED = 1, _('Reserved')
    RESERVATION_EXPIRED = 2, _('Reservation Expired')
    RESERVATION_CANCELED = 3, _('Reservation Canceled')
    WISHLIST = 4, _('Wishlist')
    PICKED_UP = 5, _('Picked Up')
