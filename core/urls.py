from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views
from .forms import ConnexionForm

urlpatterns = [
    path('', views.home, name='home'),
    path('programmes/', views.programmes_list, name='programmes_list'),
    path('programme/', RedirectView.as_view(url='/programmes/', permanent=True)),
    path('programme/<int:programme_id>/', views.programme_detail, name='programme_detail'),
    path('programme/<int:programme_id>/start/', views.defi_redirect_programme, name='defi_redirect_programme'),
    path('defi/', views.defi_redirect_actuel, name='defi_redirect_actuel'),
    path('defi/historique/', views.defis_historique, name='defis_historique'),
    path('defi/<int:semaine_id>/', views.defi_semaine, name='defi_semaine'),
    path('defi/<int:domaine_id>/domaine/', views.domaine_detail, name='domaine_detail'),
    path('defi/<int:domaine_id>/bonus/<int:action_id>/', views.commencer_bonus, name='commencer_bonus'),
    path('defi/semaine-complete/<int:semaine_id>/', views.semaine_complete, name='semaine_complete'),
    path('journal/', views.journal, name='journal'),
    path('progression/', views.progression, name='progression'),
    path('communaute/', views.communaute, name='communaute'),
    path('profil/', views.profil, name='profil'),
    path('parametres/', views.parametres, name='parametres'),

    # Adhésion Auréa
    path('rejoindre/', views.rejoindre_aurea, name='rejoindre_aurea'),
    path('rejoindre/statut/', views.statut_adhesion, name='statut_adhesion'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(authentication_form=ConnexionForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
