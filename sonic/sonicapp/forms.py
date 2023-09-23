from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
)
from django.contrib.auth.models import User
from django.forms import (
    ModelForm,
    CharField,
    EmailField,
    EmailInput,
    TextInput,
    PasswordInput,
)

from .models import PDFile


class PDFileForm(forms.ModelForm):
    class Meta:
        tailwind_class = """
        px-5
        block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 
        ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 
        focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6
        """
        model = PDFile
        exclude = ["created_at", "user"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": tailwind_class, "placeholder": "File's Title"}
            ),
            "file": forms.FileInput(
                attrs={
                    "class": tailwind_class,
                }
            ),
        }


class RegisterUserForm(UserCreationForm):
    tailwind_class = """
        px-5
        block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 
        ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 
        focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6
        """

    username = CharField(
        label="Login", widget=TextInput(attrs={"class": tailwind_class})
    )
    email = EmailField(
        label="Email", widget=EmailInput(attrs={"class": tailwind_class})
    )
    password1 = CharField(
        label="Password", widget=PasswordInput(attrs={"class": tailwind_class})
    )
    password2 = CharField(
        label="Password confirmation",
        widget=PasswordInput(attrs={"class": tailwind_class}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    tailwind_class = """
        px-5
        block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 
        ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 
        focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6
        """

    username = CharField(
        label="Login", widget=TextInput(attrs={"class": tailwind_class})
    )
    password = CharField(
        label="Password", widget=PasswordInput(attrs={"class": tailwind_class})
    )


class ResetPasswordForm(PasswordResetForm):
    tailwind_class = """
        px-5
        block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 
        ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 
        focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6
        """
    email = EmailField(
        label="Email", widget=EmailInput(attrs={"class": tailwind_class})
    )
