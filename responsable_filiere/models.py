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
class Etudiant(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_naissance = models.DateField()
    matricule = models.CharField(max_length=50, unique=True)
    date_inscription = models.DateField()
    telephone = models.CharField(max_length=20)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="etudiants", null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


# === UTILISATEURS AVEC ROLE ===
class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLES = [
        ('responsable_filiere', 'Responsable de Filière'),
        ('responsable_classe', 'Responsable de classe'),
        ('eleve', 'Elèves'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, default='eleve')
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    heure_de_debut = models.TimeField()
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

