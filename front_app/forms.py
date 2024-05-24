# forms.py
from django import forms
from library_app.models import BookReservation

STATUS_CHOICES = [
    ('wishlist', 'Wishlist'),
    ('reservation', 'Reservation')
]


class ReservationForm(forms.ModelForm):
    reservation_status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = BookReservation
        fields = ['book', 'reservation_status']
