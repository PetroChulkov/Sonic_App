import os

from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    LogoutView,
    PasswordResetConfirmView,
)
from django.contrib.messages.views import SuccessMessageMixin

from .forms import (
    PDFileForm,
    RegisterUserForm,
    LoginUserForm,
    ResetPasswordForm,
    ConfirmPasswordForm,
)
from .models import PDFile
from .model_exp import chat_response


load_dotenv()


def index(request):
    anon = request.user.is_anonymous
    if anon:
        return render(request, "sonicapp/index.html")
    pdf_files = [file.title for file in PDFile.objects.filter(user=request.user).all()]
    return render(request, "sonicapp/index.html", {"pdf_files": pdf_files})


def getResponse(request):
    userMessage = request.GET.get("userMessage")
    userSelect = request.GET.get("userSelect")
    docs = PDFile.objects.get(title=userSelect)
    query = userMessage
    doc = docs.file
    id = docs.id
    response = chat_response(doc, query, id)
    return HttpResponse(response)


def upload_file(request):
    if request.method == "POST":
        form = PDFileForm(request.POST, request.FILES, request.user.id)
        user = User.objects.filter(id=request.user.id).first()
        form.instance.user = user
        if form.is_valid():
            file = form.save()
            file.save()
            return HttpResponseRedirect("upload_file")
    else:
        form = PDFileForm()
    return render(request, "sonicapp/upload_file.html", {"form": form})


def delete_pdfile(request, id):
    pdfile = get_object_or_404(PDFile, pk=id)
    context = {"pdfile": pdfile}

    if request.method == "GET":
        return render(request, "sonicapp/post_confirm_delete.html", context)
    elif request.method == "POST":
        pdfile.delete()
        messages.success(request, "The post has been deleted successfully.")
        return redirect("pdfile_list")


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
    next_page = "login"


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = ResetPasswordForm
    template_name = "sonicapp/password_reset.html"
    email_template_name = "sonicapp/password_reset_email.html"
    html_email_template_name = "sonicapp/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "sonicapp/password_reset_subject.txt"


class PDFileListView(ListView):
    template_name = "sonicapp/pdfile_list.html"

    def get_queryset(self):
        return PDFile.objects.filter(user=self.request.user).all()


class PDFileDetailView(DetailView):
    model = PDFile
    template_name = "sonicapp/pdfile_detail.html"


class ConfirmPasswordResetView(PasswordResetConfirmView):
    form_class = ConfirmPasswordForm
