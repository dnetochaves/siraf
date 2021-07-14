from django.urls import path
from . import views

app_name = "juridico"

urlpatterns = [
    path('', views.juridico, name="juridico"),
    path('item_contratos/<int:id>/', views.item_contratos, name="item_contratos"),
    path('novo_contrato/', views.novo_contrato, name="novo_contrato"),
]