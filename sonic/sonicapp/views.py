from django.shortcuts import render
from django.http import HttpResponse, Http404
import os

from sonicapp.models import FilesUpload
from sonic import settings



# Create your views here.
def index(request):
    return render(request, "sonicapp/index.html")


def getResponse(request):
    userMessage = request.GET.get("userMessage")  # User message received from chat

    return HttpResponse(userMessage)


def home(request):
    context={"file": FilesUpload.objects.all()}
    return render(request, "sonicapp/home.html", context)

def download(requst, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open (file_path, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="aplication/filesupload")
            response["Content-Desposition"] = "inline;filename=" + os.path.basename(file_path)
            return response
    
    raise Http404