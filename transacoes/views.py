from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from categorias.models import Categoria
from core.views import MESES
from transacoes.models import Transacao

@login_required
def nova_transacao(request):
    categorias = Categoria.objects.filter(status="Ativa")

    if request.method == "POST":
        descricao = request.POST["descricao"]
        valor = request.POST["valor"]
        data = request.POST["data"]
        tipo = request.POST["tipo"]
        categoria_id = request.POST["categoria"]

        Transacao.objects.create(
            descricao=descricao,
            valor=valor,
            data=data,
            tipo=tipo,
            categoria_id=categoria_id,
        )
        return redirect("home")

    return render(request, "transacoes/nova_transacao.html", {"categorias": categorias})


@login_required
def editar_transacao(request, id):
    transacao = get_object_or_404(Transacao, id=id)
    categorias = Categoria.objects.filter(status="Ativa")

    if request.method == "POST":
        transacao.descricao = request.POST["descricao"]
        transacao.valor = request.POST["valor"]
        transacao.data = request.POST["data"]
        transacao.tipo = request.POST["tipo"]
        transacao.categoria_id = request.POST["categoria"]
        transacao.save()
        return redirect("home")

    return render(
        request,
        "transacoes/editar_transacao.html",
        {"transacao": transacao, "categorias": categorias},
    )


@login_required
def excluir_transacao(request, id):
    transacao = get_object_or_404(Transacao, id=id)

    if request.method == "POST":
        transacao.delete()
        return redirect("home")

    return render(request, "transacoes/confirmar_exclusao.html", {"transacao": transacao})

@login_required
def listar_transacoes(request):
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

    return render(request, "transacoes/listar_transacoes.html", {
        "transacoes": transacoes,
        "meses": MESES,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo,
    })