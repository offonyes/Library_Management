from django.shortcuts import render
from front_app.forms import ReservationForm


def add_reservation(request):
    form = ReservationForm()
    return render(request, 'library_app/reservation_add.html', {'form': form})


def index(request):
    return render(request, template_name='index.html')


def reservation(request):
    return render(request, template_name='library_app/reservation.html')


def reservation_history(request):
    return render(request, template_name='library_app/reservation_history.html')


def borrow(request):
    return render(request, template_name='library_app/borrow.html')


def borrow_history(request):
    return render(request, template_name='library_app/borrow_history.html')
