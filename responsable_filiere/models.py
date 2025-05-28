from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# === CLASSES ===
class Classe(models.Model):
    nom = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nom

# === SEMESTRES ===
class Semestre(models.Model):
    numero = models.PositiveSmallIntegerField(unique=True)
    nom = models.CharField(max_length=50)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='semestres')

    def __str__(self):
        return f"{self.nom} (S{self.numero})"

# === MODULES ===
class Module(models.Model):
    nom = models.CharField(max_length=100)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.nom

# === MATIERES ===
class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='matieres')
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='matieres')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='matieres')

    def __str__(self):
        return self.nom

# === PROFESSEURS ===
class Professeur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    sexe = [('M', 'Masculin'),('F', 'Féminin')]
    matieres = models.ManyToManyField(Matiere, related_name='professeurs')
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# === ETUDIANTS ===
from django.conf import settings
from django.db import models

class Etudiant(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_naissance = models.DateField()
    matricule = models.CharField(max_length=50, unique=True)
    date_inscription = models.DateField()
    telephone = models.CharField(max_length=20)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="etudiants", null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etudiant_profile'
    )
    def __str__(self):
        return f"{self.prenom} {self.nom}"




class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_de_fin = models.TimeField()
    type_evenement = models.CharField(
        max_length=50,
        choices=[('examen', 'Examen'), ('projet', 'Projet'),('reunion', 'Réunion'), ('autre', 'Autre')],
        default='examen'
    )
    classes_concernees = models.ManyToManyField(Classe)

    def __str__(self):
        return f"{self.titre} - {self.date}"

# Modèle spécifique à un examen
class Examen(models.Model):
    evenement = models.OneToOneField(Evenement, on_delete=models.CASCADE, null=True, blank=True, related_name="examens")
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.matiere.nom} - {self.evenement.date}"



from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    is_authorized = models.BooleanField(default=True)

    is_student = models.BooleanField(default=False)
    is_responsable_de_classe = models.BooleanField(default=False)
    is_responsable_de_filiere = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.email})"

    def get_role_display(self):
        if self.is_responsable_de_filiere:
            return "Responsable Filière"
        elif self.is_responsable_de_classe:
            return "Responsable de Classe"
        elif self.is_student:
            return "Élève"
        return "Autre"

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.CharField(max_length=32, default=get_random_string(32), editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande de reset pour {self.email} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
