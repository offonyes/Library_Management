from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from library_app.choice import ReservationStatus, BorrowStatus
from library_app.models import BookReservation, BooksBorrow


class BookReservationForm(forms.ModelForm):
    class Meta:
        model = BookReservation
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        status = cleaned_data.get('reservation_status')
        if book:
            if status == ReservationStatus.RESERVED:
                borrowed_count = book.borrows.filter(
                    Q(borrowed_status__in=[BorrowStatus.BORROWED, BorrowStatus.OVERDUE])).count()
                reserved_count = book.reservations.filter(reservation_status=ReservationStatus.RESERVED).count()
                total_unavailable = borrowed_count + reserved_count
                if total_unavailable >= book.stock:
                    raise ValidationError({'reservation_status': "There are no books available to reserve."
                                                                 "You can add to wishlist."})
        return cleaned_data


class BooksBorrowForm(forms.ModelForm):
    class Meta:
        model = BooksBorrow
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        status = cleaned_data.get('borrowed_status')
        if book:
            if status in [BorrowStatus.BORROWED, BorrowStatus.OVERDUE]:
                borrowed_count = book.borrows.filter(
                    Q(borrowed_status__in=[BorrowStatus.BORROWED, BorrowStatus.OVERDUE])).count()
                reserved_count = book.reservations.filter(reservation_status=ReservationStatus.RESERVED).count()
                total_unavailable = borrowed_count + reserved_count
                if total_unavailable >= book.stock:
                    raise ValidationError({'borrowed_status': "There are no books available to borrow."})

        return cleaned_data
