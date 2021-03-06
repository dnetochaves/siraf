from django.urls import path
from . import views

app_name = "juridico"

urlpatterns = [
    path('', views.juridico, name="juridico"),
    path('dados_contrato/<int:id>/', views.dados_contrato, name="dados_contrato"),
    path('dados_aditivo_valor/<int:id_contract>/<int:id_aditivo>/', views.dados_aditivo_valor, name="dados_aditivo_valor"),
    path('dados_supressao/<int:id_contract>/<int:id_supressao>/', views.dados_supressao, name="dados_supressao"),
    path('item_contratos/<int:id>/', views.item_contratos, name="item_contratos"),
    path('listar_contratos/', views.listar_contratos, name="listar_contratos"),
    path('novo_contrato/', views.novo_contrato, name="novo_contrato"),
    path('novo_aditivo_prazo/<int:id>/', views.novo_aditivo_prazo, name="novo_aditivo_prazo"),
    path('novo_aditivo_valor/<int:id>/', views.novo_aditivo_valor, name="novo_aditivo_valor"),
    path('nova_supressao/<int:id>/', views.nova_supressao, name="nova_supressao"),
    path('configurar_itens_aditivo/<int:id>/<int:id_aditivo>/', views.configurar_itens_aditivo, name="configurar_itens_aditivo"),
    path('configurar_itens_supressao/<int:id>/<int:id_supressao>/', views.configurar_itens_supressao, name="configurar_itens_supressao"),
    path('editar_contrato/<int:id>/', views.editar_contrato, name="editar_contrato"),
    path('deletar_contrato/<int:id>/', views.deletar_contrato, name="deletar_contrato"),
    path('novo_item/', views.novo_item, name="novo_item"),
    path('novo_item_aditivo_valor/', views.novo_item_aditivo_valor, name="novo_item_aditivo_valor"),
    path('novo_item_supressao/', views.novo_item_supressao, name="novo_item_supressao"),
    path('excluir_item_aditivo_valor/<int:id_contract>/<int:id_aditivo>/<int:id_item>', views.excluir_item_aditivo_valor, name="excluir_item_aditivo_valor"),
    path('novo_item_session/<int:id>/', views.novo_item_session, name="novo_item_session"),
    path('editar_item/<int:id>/', views.editar_item, name="editar_item"),
    path('deletar_item/<int:id>/', views.deletar_item, name="deletar_item"),
    path('get_item/<int:id>/<int:id_aditivo>/<int:id_item>/', views.get_item, name="get_item"),
    path('get_item_supressao/<int:id>/<int:id_supressao>/<int:id_item>/', views.get_item_supressao, name="get_item_supressao"),
    path('novo_tipo/', views.novo_tipo, name="novo_tipo"),
    path('listar_tipos/', views.listar_tipos, name="listar_tipos"),
    path('editar_tipo/<int:id>/', views.editar_tipo, name="editar_tipo"),
    path('deletar_tipo/<int:id>/', views.deletar_tipo, name="deletar_tipo"),
    path('deletar_aditivo_praso/<int:id>/', views.deletar_aditivo_praso, name="deletar_aditivo_praso"),
    path('deletar_aditivo_valor/<int:id>/', views.deletar_aditivo_valor, name="deletar_aditivo_valor"),
     path('deletar_supressao/<int:id>/', views.deletar_supressao, name="deletar_supressao"),
    path('processos/<int:id_contract>/<company>/', views.processos, name="processos")
]
