from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Registro(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE) # Vincula ao usuário

    def __str__(self):
        return self.titulo