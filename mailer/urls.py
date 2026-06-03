from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('send/', views.home),
    path('progress/', views.progress),
]