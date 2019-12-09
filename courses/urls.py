from django.contrib import admin
from django.urls import path, include
from .views import cour ,less


urlpatterns = [
    path('courses/', cour, name='courses-home'),
    path('courses/<str:course>', less , name='courses-lesson'),
]