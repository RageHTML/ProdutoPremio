from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .models import Login  
from .forms import RegisterForms, LoginForms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def logar_usuario(request):
    if request.method == "GET":
        form = LoginForms()
        return render(request, "login/login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForms(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            form_email = dados['email']
            senha_digitada = dados['password']

            try:
                user_mail = User.objects.get(email=form_email)
                user = authenticate(request, username=user_mail.username, password=senha_digitada)

                if user is not None:
                    login(request, user)
                    return redirect('/produtopremio/dashboard')
                else:
                    form.add_error(None, "Email ou senha incorretos")
            except User.DoesNotExist:
                form.add_error(None, "Usuario nao encontrado")
                
        return render(request, "login/login.html", {"form": form})

def registrar_usuario(request): 
    if request.method == "GET":
        form = RegisterForms()
        return render(request, "register/register.html", {"form": form})
    elif request.method == "POST":
        form = RegisterForms(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/account/login")
        else:
            return render(request, "register/register.html", {"form": form})