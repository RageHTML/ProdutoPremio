from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("account/", include("reglog.urls")),
    path("produtopremio/", include("dashboard.urls")),
    path("admin/", admin.site.urls),
    path("profile/", include("myprofile.urls"))
]