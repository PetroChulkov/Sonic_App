from django import forms
from .models import PDFile


class PDFileForm(forms.ModelForm):
    class Meta:
        model = PDFile
        exclude = ["created_at", "text"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "File's Title"}
            ),
        }
