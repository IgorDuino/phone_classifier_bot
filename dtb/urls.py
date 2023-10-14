import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from classifier.views import download_file

urlpatterns = [
    path("", lambda request: redirect("admin/")),
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path("download/<str:file_name>/", download_file, name="download_file"),
]
