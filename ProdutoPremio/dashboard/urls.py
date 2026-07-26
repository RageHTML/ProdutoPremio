from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.carregar_dashboard, name="dashboard"),
]