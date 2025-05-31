from django.urls import path
from . import views

urlpatterns = [
    path('generate_post/', views.generate_post, name='generate_post'),
]