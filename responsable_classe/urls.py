from django.urls import path
from . import views

urlpatterns = [
    # Ajoute tes routes ici, exemple :
    path('', views.index, name='classe_index'),
]