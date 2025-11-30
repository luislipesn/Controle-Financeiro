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


class Transacao(models.Model):
    TIPO_CHOICES = (
        ("receita", "Receita"),
        ("despesa", "Despesa"),
    )

    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.descricao} - {self.valor}"


class RelatorioMensal(models.Model):
    mes = models.IntegerField()
    ano = models.IntegerField()
    totalReceitas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    totalDespesas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.mes}/{self.ano}"
