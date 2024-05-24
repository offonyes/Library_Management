from django.urls import path

from accounts_app.views import login_register

urlpatterns = [
    path("", login_register, name="reg"),
]
