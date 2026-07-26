from django.urls import path

from . import views

urlpatterns = [
    path("myprofile/", views.carregar_profile, name="profile_usuario"),
    path("logout/", views.logout_usuario, name="logout")
]