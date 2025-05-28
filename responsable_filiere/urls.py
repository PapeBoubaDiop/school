from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    # Matières
    path('matieres/', views.liste_matieres, name='liste_matieres'),
    path('matieres/ajouter/', views.ajouter_matiere, name='ajouter_matiere'),
    path('matieres/modifier/<int:matiere_id>/', views.edit_matiere, name='edit_matiere'),
    path('matieres/delete/<int:matiere_id>/', views.supprimer_matiere, name='supprimer_matiere'),


    # Modules
    path('modules/', views.liste_modules, name='liste_modules'),
    path('modules/ajouter/', views.ajouter_module, name='ajouter_module'),
    path('modules/modifier/<int:module_id>/', views.edit_module, name='edit_module'),
    path('modules/delete/<int:module_id>/', views.supprimer_module, name='supprimer_module'),

    # Professeurs
    path('professeurs/', views.liste_professeurs, name='liste_professeurs'),
    path('professeurs/ajouter/', views.ajouter_professeur, name='ajouter_professeur'),
    path('professeurs/modifier/<int:professeur_id>', views.edit_professeur, name='edit_professeur'),
    path('professeurs/delete/<int:professeur_id>/', views.supprimer_professeur, name='supprimer_professeur'),


    # Semestres
    path('semestres/', views.liste_semestres, name='liste_semestres'),
    path('semestres/ajouter/', views.ajouter_semestre, name='ajouter_semestre'),
    path('semestres/modifier/<int:semestre_id>/', views.modifier_semestre, name='modifier_semestre'),
    path('semestres/supprimer/<int:semestre_id>/', views.supprimer_semestre, name='supprimer_semestre'),



    # Étudiants
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path("etudiants/ajouter/", views.ajouter_etudiant, name="ajouter_etudiant"),
    path('etudiants/modifier/<int:etudiant_id>', views.edit_etudiant, name='edit_etudiant'),
    path('etudiants/delete/<int:etudiant_id>', views.supprimer_etudiant, name='supprimer_etudiant'),

    # Evenements
    path('evenements/', views.liste_evenements, name='liste_evenements'),
    path('evenements/ajouter/', views.ajouter_evenement, name='ajouter_evenement'),
    path('evenements/json/', views.events_json, name='events_json'),

    # Examens
    path('examens/', views.examens, name='examens'),
    path('examens/ajouter/', views.ajouter_examen, name='ajouter_examen'),
    path('examens/modifier/<int:examen_id>', views.edit_examen, name='edit_examen'),
    path('get_matieres/<int:classe_id>/', views.get_matieres, name='get_matieres'),
    path('evenements/', views.evenements, name='evenements'),


    # Authentification
    path('comptes/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('comptes/ajouter', views.creation_comptes_etudiants, name='creation_comptes_etudiants'),
    path('comptes/toggle/<int:user_id>/', views.toggle_activation, name='toggle_activation'),


    # Login and Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password Reset
    path('changer-mot-de-passe/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html',
        success_url='/changer-mot-de-passe-fait/'
    ), name='password_change'),
    path('changer-mot-de-passe-fait/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'
    ), name='password_change_done'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])