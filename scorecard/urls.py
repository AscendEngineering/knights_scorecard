from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', mainPage, name="mainPage"),
    path('knight/<name>/', knightsPage, name="knightsPage"),
]
