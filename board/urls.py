"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views import View

from board import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("rewrite_process", views.rewrite_process, name="rewrite_process"),
    path("rewrite", views.rewrite, name="rewrite"),
    path("delete", views.delete, name="delete"),
    path("view", views.view_post, name="view"),
    path("write_process", views.write_process, name="write_process"),
    path("write", views.write, name="write"),
    path("", views.index, name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)