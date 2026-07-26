from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.registrar_usuario, name="register"),
    path("login/", views.logar_usuario, name="login"),
]