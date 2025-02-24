from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import liste_annonces, detail_annonce
from . import views
urlpatterns = [
    path('', liste_annonces, name='liste_annonces'),
    path('liste-annonce/<int:pk>', detail_annonce,name='detail_annonce')
]

