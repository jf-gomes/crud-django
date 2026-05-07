from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# aqui é criado o modelo do item gerenciado pelo sistema.
class Registro(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE) # vinculação ao usuário.

    def __str__(self):
        return self.titulo