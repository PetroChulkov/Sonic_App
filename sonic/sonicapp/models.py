from django.db import models


# Create your models here.
class PDFile(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="uploads/")
    text = models.TextField(default="")

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    question = models.CharField(max_length=500)
    pdf_file = models.ForeignKey(
        PDFile, related_name="question", on_delete=models.CASCADE
    )
