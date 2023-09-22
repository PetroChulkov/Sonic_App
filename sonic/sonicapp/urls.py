from django.urls import path
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("getResponse", views.getResponse, name="getResponse"),
    path("upload_file", views.upload_file, name="upload_file"),
    path("<int:pk>", views.PDFileDetailView.as_view(), name="pdfile_detail"),
    path("myfiles", views.PDFileListView.as_view(), name="pdfile_list"),
    path("register/", views.RegisterUser.as_view(), name="register"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.LogOutUser.as_view(), name="logout"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(
            template_name="sonicapp/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="sonicapp/password_reset_confirm.html",
            success_url="/reset-password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        PasswordResetCompleteView.as_view(
            template_name="sonicapp/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
