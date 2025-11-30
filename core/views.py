from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transacoes.models import Transacao
from django.db import models




MESES = [
    (1, "Janeiro"),
    (2, "Fevereiro"),
    (3, "Março"),
    (4, "Abril"),
    (5, "Maio"),
    (6, "Junho"),
    (7, "Julho"),
    (8, "Agosto"),
    (9, "Setembro"),
    (10, "Outubro"),
    (11, "Novembro"),
    (12, "Dezembro"),
]

@login_required
def home(request):
    hoje = date.today()
    mes = hoje.month
    ano = hoje.year

    # Transações do mês
    transacoes_mes = Transacao.objects.filter(data__month=mes, data__year=ano)

    receitas = transacoes_mes.filter(tipo="R").aggregate(total=models.Sum("valor"))["total"] or 0
    despesas = transacoes_mes.filter(tipo="D").aggregate(total=models.Sum("valor"))["total"] or 0
    saldo = receitas - despesas

    # Últimas 5 transações
    ultimas = Transacao.objects.order_by("-data")[:5]

    # Resumo anual
    transacoes_ano = Transacao.objects.filter(data__year=ano)
    receitas_ano = transacoes_ano.filter(tipo="R").aggregate(total=models.Sum("valor"))["total"] or 0
    despesas_ano = transacoes_ano.filter(tipo="D").aggregate(total=models.Sum("valor"))["total"] or 0
    saldo_ano = receitas_ano - despesas_ano

    contexto = {
        "receitas": receitas,
        "despesas": despesas,
        "saldo": saldo,
        "ultimas": ultimas,
        "receitas_ano": receitas_ano,
        "despesas_ano": despesas_ano,
        "saldo_ano": saldo_ano,
        "mes_atual": mes,
        "ano_atual": ano,
    }

    return render(request, "core/dashboard.html", contexto)