from django.contrib import admin
from django.urls import path, include
from .views import cour ,less


urlpatterns = [
    path('', cour, name='courses-home'),
    path('course/<str:course>/', less , name='courses-lesson'),
]