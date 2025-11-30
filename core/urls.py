from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('nova/', views.nova_transacao, name="nova_transacao"),
    path('editar/<int:id>/', views.editar_transacao, name="editar_transacao"),
    path('excluir/<int:id>/', views.excluir_transacao, name="excluir_transacao"),

    path('categorias/', views.listar_categorias, name="listar_categorias"),
    path('categorias/nova/', views.nova_categoria, name="nova_categoria"),
    path('categorias/editar/<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('categorias/desativar/<int:id>/', views.desativar_categoria, name="desativar_categoria"),
    path('categorias/excluir/<int:id>/', views.excluir_categoria, name="excluir_categoria"),

    path("relatorio/", views.relatorio, name="relatorio"),

]
