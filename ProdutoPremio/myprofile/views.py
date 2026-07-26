from django.http import HttpResponse
from django.shortcuts import render, redirect
from reglog.models import Usuarios
from django.contrib.auth.models import User


def carregar_profile(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/account/register")
        else:
            username = request.user.get_username()
            return render(request, "profile/profile.html",{'username': username})
