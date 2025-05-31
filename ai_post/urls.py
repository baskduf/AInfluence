from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.auto_generate_post, name='auto_generate_post'),
]