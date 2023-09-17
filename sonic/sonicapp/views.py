from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PDFileForm


# Create your views here.
def index(request):
    return render(request, "sonicapp/index.html")


def getResponse(request):
    userMessage = request.GET.get("userMessage")  # User message received from chat

    return HttpResponse(userMessage)


def upload_file(request):
    if request.method == "POST":
        form = PDFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            file.save()
            print(request.FILES, request.POST)
            return HttpResponseRedirect("upload_file")
    else:
        form = PDFileForm()
    return render(request, "sonicapp/upload_file.html", {"form": form})
