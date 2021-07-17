from django.urls import path
from . import views

app_name = "juridico"

urlpatterns = [
    path('', views.juridico, name="juridico"),
    path('item_contratos/<int:id>/', views.item_contratos, name="item_contratos"),
    path('listar_contratos/', views.listar_contratos, name="listar_contratos"),
    path('novo_contrato/', views.novo_contrato, name="novo_contrato"),
    path('editar_contrato/<int:id>/', views.editar_contrato, name="editar_contrato"),
    path('deletar_contrato/<int:id>/', views.deletar_contrato, name="deletar_contrato"),
    path('novo_item/', views.novo_item, name="novo_item"),
    path('editar_item/<int:id>/', views.editar_item, name="editar_item"),
    path('deletar_item/<int:id>/', views.deletar_item, name="deletar_item"),
]