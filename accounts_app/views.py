from django.http import HttpResponse
from django.shortcuts import render

from accounts_app.forms import LoginForm, RegisterForm


def login_register(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == "POST":
        if "register" in request.POST:
            text = """
            <p> Congratulation you have successfully registered.</p>
            """
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.save()
                return HttpResponse(text)
    return render(
        request,
        "accounts_app/log_reg.html",
        {"login_form": login_form, "register_form": register_form, "is_active": True},
    )
