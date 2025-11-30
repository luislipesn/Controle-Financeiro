from django.db import models

from categorias.models import Categoria

class Transacao(models.Model):
    TIPO_CHOICES = (
        ("R", "Receita"),
        ("D", "Despesa"),
    )

    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.descricao} - {self.valor}"

