from django.urls import path
from . import views

urlpatterns = [
    # Ajoute tes routes ici, exemple :
    path('', views.index, name='dashboard_responsable_classe'),
    path('matieres/', views.matieres_view, name='matieres_view'),
    path('professeurs/', views.professeurs_view, name='professeurs_view'),
    path('etudiants/', views.etudiants_view, name='etudiants_view'),
    path('evaluations/', views.evenements_examens_view, name='evenements_examens_view'),
    path('emploi_du_temps/', views.emploi_du_temps_view, name='emploi_du_temps_view'),
    path('seance/<int:seance_id>/absences/', views.absences_seance, name='absences_seance'),
    path('cahier_texte/', views.cahier_texte, name='cahier_texte'),
    path('cahier-texte/seance/<int:seance_id>/', views.ajouter_lecon_seance, name='ajouter_lecon_seance'),
]