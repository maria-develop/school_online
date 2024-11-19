from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ims/", include("ims.urls", namespace="ims"))
]
