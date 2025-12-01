from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from categorias.models import Categoria
from core.views import MESES
import csv
from transacoes.models import Transacao
from django.db.models import Sum
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

@login_required
def gerar_pdf_profissional(transacoes, filtros):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elementos = []

    # Título
    titulo = Paragraph("<b>Relatório Financeiro</b>", styles["Title"])
    elementos.append(titulo)
    elementos.append(Spacer(1, 12))

    # Filtros aplicados
    filtro_texto = "<b>Filtros aplicados:</b><br/>"
    for nome, valor in filtros.items():
        if valor:
            filtro_texto += f"- {nome}: {valor}<br/>"

    elementos.append(Paragraph(filtro_texto, styles["Normal"]))
    elementos.append(Spacer(1, 12))

    # Cabeçalho da tabela
    dados = [["Data", "Descrição", "Tipo", "Categoria", "Valor (R$)"]]

    # Linhas da tabela
    for t in transacoes:
        dados.append([
            t.data.strftime("%d/%m/%Y"),
            t.descricao,
            "Receita" if t.tipo == "R" else "Despesa",
            t.categoria.nome,
            f"{t.valor:.2f}",
        ])

    # Criando tabela
    tabela = Table(dados, colWidths=[70, 160, 70, 90, 70])

    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ]))

    elementos.append(tabela)
    doc.build(elementos)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf

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
    
    if request.GET.get("export") == "csv":

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_financeiro.csv"'

        writer = csv.writer(response)
        writer.writerow(["Data", "Descrição", "Tipo", "Categoria", "Valor"])

        for t in transacoes:
            writer.writerow([
                t.data,
                t.descricao,
                "Receita" if t.tipo == "R" else "Despesa",
                t.categoria.nome,
                float(t.valor)
            ])

        return response
    
    # EXPORTAÇÃO PDF
    if request.GET.get("export") == "pdf":
        from django.http import HttpResponse

        filtros_usados = {
        "Mês": request.GET.get("mes"),
        "Ano": request.GET.get("ano"),
        "Data início": request.GET.get("data_inicio"),
        "Data fim": request.GET.get("data_fim"),
        "Categoria": request.GET.get("categoria"),
        }

        pdf = gerar_pdf_profissional(transacoes, filtros_usados)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="relatorio_financeiro.pdf"'

        response.write(pdf)
        return response

    return render(request, "relatorios/relatorio.html", {
        "transacoes": transacoes,
        "meses": MESES,
        "categorias": categorias,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo
    })

    

