from django.shortcuts import get_object_or_404, render, redirect
from .models import Transacao, Categoria
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


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
    total_receitas = transacoes.filter(tipo="receita").aggregate(Sum("valor"))["valor__sum"] or 0
    total_despesas = transacoes.filter(tipo="despesa").aggregate(Sum("valor"))["valor__sum"] or 0
    saldo = total_receitas - total_despesas

    return render(request, "home.html", {
        "transacoes": transacoes,
        "meses": MESES,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo,
    })


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

    return render(request, "nova_transacao.html", {"categorias": categorias})


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
        "editar_transacao.html",
        {"transacao": transacao, "categorias": categorias},
    )


@login_required
def excluir_transacao(request, id):
    transacao = get_object_or_404(Transacao, id=id)

    if request.method == "POST":
        transacao.delete()
        return redirect("home")

    return render(request, "confirmar_exclusao.html", {"transacao": transacao})


from django.contrib import messages


@login_required
def listar_categorias(request):
    categorias = Categoria.objects.exclude(status="Excluída")
    return render(request, "categorias/listar.html", {"categorias": categorias})

@login_required
def nova_categoria(request):
    if request.method == "POST":
        nome = request.POST["nome"]

        Categoria.objects.create(nome=nome, status="Ativa")
        messages.success(request, "Categoria criada com sucesso!")
        return redirect("listar_categorias")

    return render(request, "categorias/nova.html")

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == "POST":
        categoria.nome = request.POST["nome"]
        categoria.status = request.POST["status"]
        categoria.save()
        messages.success(request, "Categoria atualizada!")
        return redirect("listar_categorias")

    return render(request, "categorias/editar.html", {"categoria": categoria})

@login_required
def desativar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.status = "Inativa"
    categoria.save()
    messages.warning(request, "Categoria desativada!")
    return redirect("listar_categorias")

@login_required
def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if Transacao.objects.filter(categoria=categoria).exists():
        messages.error(request, "Não é possível excluir: existem transações usando esta categoria.")
        return redirect("listar_categorias")

    categoria.status = "Excluída"  
    categoria.save()
    messages.success(request, "Categoria excluída!")
    return redirect("listar_categorias")

@login_required
def relatorio(request):

    transacoes = Transacao.objects.all().order_by("-data")

    mes = request.GET.get("mes")
    ano = request.GET.get("ano")
    data_inicio = request.GET.get("data_inicio") or None
    data_fim = request.GET.get("data_fim") or None
    categoria = request.GET.get("categoria")

    # FILTRO POR MÊS + ANO
    if mes and ano:
        transacoes = transacoes.filter(
            data__month=int(mes),
            data__year=int(ano)
        )

    # FILTRO POR PERÍODO
    if data_inicio and data_inicio.strip():
        transacoes = transacoes.filter(data__gte=data_inicio)

    if data_fim and data_fim.strip():
        transacoes = transacoes.filter(data__lte=data_fim)

    # FILTRO POR CATEGORIA
    if categoria:
        transacoes = transacoes.filter(categoria_id=categoria)

    # RESUMO DO RELATÓRIO
    total_receitas = transacoes.filter(tipo__iexact="R").aggregate(Sum("valor"))['valor__sum'] or 0
    total_despesas = transacoes.filter(tipo__iexact="D").aggregate(Sum("valor"))['valor__sum'] or 0
    saldo = total_receitas - total_despesas

    categorias = Categoria.objects.exclude(status="Excluída")

    return render(request, "relatorios/relatorio.html", {
        "transacoes": transacoes,
        "meses": MESES,
        "categorias": categorias,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo
    })
