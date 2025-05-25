from django.contrib import admin
from .models import Classe, Semestre, Module, Matiere, Professeur, Etudiant, Examen, Utilisateur, Evenement

admin.site.register(Classe)
admin.site.register(Semestre)
admin.site.register(Module)
admin.site.register(Matiere)
admin.site.register(Professeur)
admin.site.register(Etudiant)
admin.site.register(Examen)
admin.site.register(Evenement)
admin.site.register(Utilisateur)
