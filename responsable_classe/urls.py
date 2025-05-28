from django.urls import path
from . import views

urlpatterns = [
    # Ajoute tes routes ici, exemple :
    path('', views.index, name='dashboard_responsable_classe'),
    path('matieres/', views.matieres_view, name='matieres_view'),
]