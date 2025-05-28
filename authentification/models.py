# models.py (dans ton app users par exemple)
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_authorized = models.BooleanField(default=True)

    is_student = models.BooleanField(default=False)
    is_responsable_de_classe = models.BooleanField(default=False)
    is_responsable_de_filiere = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.CharField(max_length=32, default=get_random_string(32), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
