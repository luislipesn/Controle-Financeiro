from django.db import models

class Categoria(models.Model):
    STATUS_CHOICES = (
        ("Ativa", "Ativa"),
        ("Inativa", "Inativa"),
        ("Excluída", "Excluída"),
    )

    nome = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Ativa")

    def __str__(self):
        return self.nome

