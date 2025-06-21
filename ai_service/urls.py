from django.urls import path
from . import views

urlpatterns = [
    path('generate_post/', views.generate_post, name='generate_post'),
    path('trigger_generate/', views.trigger_generate, name='trigger_generate'),  # ❗ 이거 추가돼야 함
]