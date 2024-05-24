from django.urls import path
from front_app.views import index, reservation, reservation_history, borrow, borrow_history, add_reservation


urlpatterns = [
    path('index/', index, name='index'),
    path('reservations/', reservation, name='reservation'),
    path('reservations/add/', add_reservation, name='add_reservation'),
    path('reservations/history/', reservation_history, name='reservation_history'),
    path('borrow/', borrow, name='borrow'),
    path('borrow/history/', borrow_history, name='borrow_history'),
]
