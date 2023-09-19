import os

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from langchain.document_loaders import PyPDFLoader

from langchain.text_splitter import CharacterTextSplitter

from langchain.text_splitter import RecursiveCharacterTextSplitter

from .forms import PDFileForm, RegisterUserForm, LoginUserForm
from .models import PDFile

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





class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "sonicapp/register.html"
    success_url = reverse_lazy("sonicapp:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "sonicapp/login.html"


class LogOutUser(LogoutView):
    next_page = "/"


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "sonicapp/password_reset.html"
    email_template_name = "sonicapp/password_reset_email.html"
    html_email_template_name = "sonicapp/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "sonicapp/password_reset_subject.txt"

