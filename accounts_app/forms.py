from django import forms
from accounts_app.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        email = self.cleaned_data["email"]
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Please enter a valid email address.")
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        return password


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    personal_number = forms.CharField(max_length=11)
    email = forms.EmailField(max_length=100)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "personal_number",
            "birth_date",
            "password1",
            "password2",
        )
