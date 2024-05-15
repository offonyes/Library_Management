from django.urls import path

from accounts_app.views import login_register, redirecting_view, log_out

urlpatterns = [
    path("", login_register, name="reg"),
    path("main/", redirecting_view, name="main"),
    path("", log_out, name="logout"),
]
