from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views, views_admin
urlpatterns = [
    
    path('', views.portfolio_page, name='portfolio'),  # Page portfolio (page d'accueil principale)
    path('app/', liste_annonces, name='liste_annonces'),  # Application d'annonces
    path('mes-annonces/', liste_annonces_user, name='liste_annonces_user'),
    path('annonces/<int:annonce_id>/', detail_annonce, name='detail_annonce'),
    path('creer/', views.creer_annonce, name='creer_annonce'),
    path('modifier/<int:annonce_id>/', views.modifier_annonce, name='modifier_annonce'),
    path('supprimer/<int:annonce_id>/', views.supprimer_annonce, name='supprimer_annonce'),
    
    
    
    path('admins/', views_admin.admin_dashboard, name='admin_dashboard'),
    path('admins/valider/<int:annonce_id>/', views_admin.valider_annonce, name='valider_annonce'),
    path('admins/modifier/<int:annonce_id>/', views_admin.modifier_annonce_admin, name='modifier_annonce_admin'),
    path('admins/supprimer/<int:annonce_id>/', views_admin.supprimer_annonce_admin, name='supprimer_annonce_admin'),
    path('admins/creer/', views_admin.creer_annonce_admin, name='creer_annonce_admin'),
    path('admins/categories/', views_admin.liste_categories, name='liste_categories'),
    path('admins/categories/creer/', views_admin.creer_categorie, name='creer_categorie'),
    path('admins/categories/modifier/<int:categorie_id>/', views_admin.modifier_categorie, name='modifier_categorie'),
    path('admins/categories/supprimer/<int:categorie_id>/', views_admin.supprimer_categorie, name='supprimer_categorie'),
]

