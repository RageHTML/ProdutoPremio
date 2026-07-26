from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout


def carregar_profile(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/account/register")
        else:
            username = request.user.get_username()
            return render(request, "profile/profile.html",{'username': username})

def logout_usuario(request):
    if request.method == "GET":
        return redirect("/profile/myprofile")
    elif request.method == "POST":
        logout(request) 
        return redirect('login') 
