from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

    @property
    def cargo(self):
        """
        Retorna o nome do primeiro grupo associado ao usuário.
        Caso o usuário não esteja em nenhum grupo, retorna 'Sem grupo'.
        """
        grupos = self.groups.all()
        if grupos.exists():
            return grupos.first().name
        return "Sem grupo"

    def __str__(self):
        return self.username

