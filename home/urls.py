from django.contrib import admin
from django.urls import path, include
from .views import starting, about, member, membersh, callfun, profile_view, cancelSubscription


urlpatterns = [
    # path('', starting, name='home-home'),
    path('about/', about , name='home-about'),
    path('memberships/', member , name='home-memberships'),
    path('memberships/<str:key>/', membersh , name='home-memberships-indi'),
    path('membership/<str:key>/', callfun , name='home-memberships-indiv'),
    path('profile/', profile_view , name='profileview'),
    path('cancelsub/', cancelSubscription , name='cancelsub'),
]