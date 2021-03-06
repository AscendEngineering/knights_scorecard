from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *
from django.conf.urls import url

urlpatterns = [
    path('',splashPage,name="splashPage"),
    path('metrics/', getMetrics, name='getMetrics'),
    url('auth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', splashPage, name='login'),
    url(r'^logout/$', logout, name='logout'),  
    url('access_denied/',access_denied,name='access_denied'),
    url('scorecard/',scorecard,name='scorecard'),
   # url('webhooks/',webhook,name='webhook')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
