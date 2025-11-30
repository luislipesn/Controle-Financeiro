from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_categorias, name="listar_categorias"),
    path("nova/", views.nova_categoria, name="nova_categoria"),
    path("editar/<int:id>/", views.editar_categoria, name="editar_categoria"),
    path("desativar/<int:id>/", views.desativar_categoria, name="desativar_categoria"),
    path("excluir/<int:id>/", views.excluir_categoria, name="excluir_categoria"),
]
