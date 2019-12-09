from django.contrib import admin
from django.urls import path, include
from .views import starting, about


urlpatterns = [
    path('', starting, name='home-home'),
    path('about/', about , name='home-about'),
]