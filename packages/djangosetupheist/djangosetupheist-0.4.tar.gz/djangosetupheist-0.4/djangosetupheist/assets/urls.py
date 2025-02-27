from django.contrib import admin
from django.urls import path, include

from .appsConfig import getAppUrls

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += getAppUrls()