from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),        # 👈 THIS FIXES YOUR ERROR
    path('send/', views.send_test_email),
]