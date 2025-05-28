from django.contrib import admin
from .models import Absence, Seance, Classe, Semestre, Module, Matiere, Professeur, CustomUser, Etudiant, Examen, Evenement

admin.site.register(Classe)
admin.site.register(Semestre)
admin.site.register(Module)
admin.site.register(Matiere)
admin.site.register(Professeur)
admin.site.register(Etudiant)
admin.site.register(Examen)
admin.site.register(Evenement)
admin.site.register(Seance)
admin.site.register(Absence)
# admin.site.register(CustomUser)

from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_authorized', 'is_superuser')
    list_filter = ('is_active', 'is_authorized', 'is_superuser')
    search_fields = ('username', 'email')