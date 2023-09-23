from datetime import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse


class PDFile(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="uploads/")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("pdfile_detail", args=[str(self.id)])


class Question(models.Model):
    question = models.CharField(max_length=500)
    pdf_file = models.ForeignKey(
        PDFile, related_name="question", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
