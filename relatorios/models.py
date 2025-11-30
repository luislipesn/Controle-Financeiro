from django.db import models

class RelatorioMensal(models.Model):
    mes = models.IntegerField()
    ano = models.IntegerField()
    totalReceitas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    totalDespesas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.mes}/{self.ano}"
