from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("getResponse", views.getResponse, name="getResponse"),
    path("upload_file", views.upload_file, name="upload_file"),
]
