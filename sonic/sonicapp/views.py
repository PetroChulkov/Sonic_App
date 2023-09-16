from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, "sonicapp/index.html")


def getResponse(request):
    userMessage = request.GET.get("userMessage")  # User message received from chat

    return HttpResponse(userMessage)
