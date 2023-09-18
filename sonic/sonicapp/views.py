from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PDFileForm
from .models import PDFile
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sonic.settings import BASE_DIR
from .models import PDFile


# Create your views here.
def index(request):
    pdf_files = [file.title for file in PDFile.objects.all()]
    return render(request, "sonicapp/index.html", {"pdf_files": pdf_files})


def getResponse(request):
    userMessage = request.GET.get("userMessage")  # User message received from chat
    userSelect = request.GET.get("userSelect")  # User message received from chat
    print(request.GET)
    return HttpResponse(userMessage)


def upload_file(request):
    if request.method == "POST":
        form = PDFileForm(request.POST, request.FILES)
        if form.is_valid():
            text = text_extractor(
                os.path.join(
                    BASE_DIR, "media", "uploads", form.cleaned_data["file"].name
                )
            )
            file = form.save()
            file.text = text
            file.save()
            return HttpResponseRedirect("upload_file")
    else:
        form = PDFileForm()
    return render(request, "sonicapp/upload_file.html", {"form": form})


def text_extractor(file):
    loader = PyPDFLoader(file)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(data)
    text = [t.page_content for t in docs]
    return text
