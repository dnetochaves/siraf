from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    name = models.CharField(max_length=100)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.name