from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts_app.forms import LoginForm, RegisterForm


def login_register(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == "POST":
        if "login" in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("profile")
                else:
                    return render(
                        request,
                        "accounts_app/log_reg.html",
                        {
                            "login_form": login_form,
                            "register_form": register_form,
                            "is_active": False,
                        },
                    )
        elif "register" in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                # user.is_active = False
                user.save()
                # activateEmail()
                return render(request, "index.html")
    return render(
        request,
        "accounts_app/log_reg.html",
        {"login_form": login_form, "register_form": register_form, "is_active": True},
    )


@login_required(login_url="/")
def redirecting_view(request):
    return render(request, "index.html")


def log_out(request):
    logout(request)
    return redirect("logout")
