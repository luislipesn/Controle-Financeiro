from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from categorias.models import Categoria
from transacoes.models import Transacao


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
