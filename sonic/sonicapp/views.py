from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PDFileForm
from .models import PDFile
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from sonic.settings import BASE_DIR
from .models import PDFile
from .model_exp import text_extractor, get_vectorstore, get_conversation_chain

# Create your views here.
def index(request):
    pdf_files = [file.title for file in PDFile.objects.all()]
    return render(request, "sonicapp/index.html", {"pdf_files": pdf_files})


def getResponse(request):
    userMessage = request.GET.get("userMessage")  # User message received from chat
    userSelect = request.GET.get("userSelect")  # User message received from chat
    print(request.GET)
    docs = PDFile.objects.get(title=userSelect)
    vectorscore = get_vectorstore(docs.text)
    response = get_conversation_chain(vectorscore, userMessage)
    return HttpResponse(response)


def upload_file(request):
    if request.method == "POST":
        form = PDFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            text = text_extractor(
                os.path.join(
                    BASE_DIR, "media", "uploads", form.cleaned_data["file"].name
                )
            )
            file.text = text
            file.save()
            return HttpResponseRedirect("upload_file")
    else:
        form = PDFileForm()
    return render(request, "sonicapp/upload_file.html", {"form": form})



