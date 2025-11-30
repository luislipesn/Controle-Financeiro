from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_transacoes, name="listar_transacoes"),
    path("nova/", views.nova_transacao, name="nova_transacao"),
    path("editar/<int:id>/", views.editar_transacao, name="editar_transacao"),
    path("excluir/<int:id>/", views.excluir_transacao, name="excluir_transacao"),
]