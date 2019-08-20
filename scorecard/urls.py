from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('',splashPage,name="splashPage"),
    path('main/', mainPage, name="mainPage"),
    path('main/knight/', knightsPage, name="knightsPage"),
    path('metrics/', getMetrics, name='getMetrics'),
    path('authenticate',authenticateUser,name='authenticateUser'),
    path('authorize',authorizeUser,name='authorizeUser'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
