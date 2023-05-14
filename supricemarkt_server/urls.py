from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('main', include('web_scrapping.urls')),
]


