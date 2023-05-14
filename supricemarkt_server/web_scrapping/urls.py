from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('/api/search', views.getMainData, name='scrapedata'),
    path('/api/search/dia', views.getDiaData, name='scrapedataDia'),
    path('/api/search/carrefour', views.getCarrefourData, name='scrapedataCarrefour'),
    path('/api/search/ahorra', views.getAhorraMasData, name='scrapedataAhorra'), 
]


