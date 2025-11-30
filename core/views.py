from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from transacoes.models import Transacao


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
    transacoes = Transacao.objects.all().order_by("-data")

    mes = request.GET.get("mes")
    ano = request.GET.get("ano")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    # FILTRO POR MÊS + ANO
    if mes and ano:
        transacoes = transacoes.filter(data__month=mes, data__year=ano)

    # FILTRO POR PERÍODO DE DATAS
    if data_inicio:
        transacoes = transacoes.filter(data__gte=data_inicio)

    if data_fim:
        transacoes = transacoes.filter(data__lte=data_fim)

    # RESUMO MENSAL (cardzinhos)
    total_receitas = transacoes.filter(tipo="R").aggregate(Sum("valor"))["valor__sum"] or 0
    total_despesas = transacoes.filter(tipo="D").aggregate(Sum("valor"))["valor__sum"] or 0
    saldo = total_receitas - total_despesas

    return render(request, "home.html", {
        "transacoes": transacoes,
        "meses": MESES,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo,
    })