from django import forms
from .models import PDFile

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.forms import (
    ModelForm,
    CharField,
    EmailField,
    EmailInput,
    TextInput,
    PasswordInput,
)


class PDFileForm(forms.ModelForm):
    class Meta:
        model = PDFile
        exclude = ["created_at", "text"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "File's Title"}
            ),
        }


class RegisterUserForm(UserCreationForm):
    username = CharField(label="Login", widget=TextInput(attrs={"class": "form-input"}))
    email = EmailField(label="Email", widget=EmailInput(attrs={"class": "form-input"}))
    password1 = CharField(
        label="Password", widget=PasswordInput(attrs={"class": "form-input"})
    )
    password2 = CharField(
        label="Password confirmation",
        widget=PasswordInput(attrs={"class": "form-input"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = CharField(label="Login", widget=TextInput(attrs={"class": "form-input"}))
    password = CharField(
        label="Password", widget=PasswordInput(attrs={"class": "form-input"})
    )
