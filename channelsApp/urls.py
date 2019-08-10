# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.chatindex, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]