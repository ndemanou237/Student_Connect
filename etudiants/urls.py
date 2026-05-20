from django.urls import path
from . import views

app_name = 'etudiants'

urlpatterns = [
     path('', views.accueil, name='accueil'),
     path('contact/', views.contact, name='contact'),
     path('inscription/', views.inscription, name='inscription'),
     path('connexion/', views.connexion_vue ,name='connexion'),
     path('deconnexion/', views.deconnexion_vue, name='deconnexion'),
     path('deposer/', views.deposer_portfolio, name='deposer'),
     path('mon-espace', views.mon_espace, name='mon_espace'),
     path('modifier/', views.modifier_profil, name='modifier'),
     path('supprimer/', views.supprimer_profil, name='supprimer'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('valider/<int:etudiant_id>', views.valider_porfolio, name='valider'),
     path('rejeter/<int:etudiant_id>', views.rejeter_porfolio, name='rejeter'),
]
