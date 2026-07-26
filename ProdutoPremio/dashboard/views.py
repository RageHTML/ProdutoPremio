from django.http import HttpResponse
from django.shortcuts import render, redirect
from reglog.models import Usuarios
from django.contrib.auth.models import User


def carregar_dashboard(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/account/register")

        username = User.objects.all().values_list('username', flat=True)
        email = User.objects.all().values_list('email', flat=True)
        password = User.objects.all().values_list('password', flat=True)
        return render(request, "home/home.html", {'username':username,'email':email,'password':password})
