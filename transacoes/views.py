from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from categorias.models import Categoria
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

# Create your views here.
