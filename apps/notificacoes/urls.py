from django.urls import path
from . import views

app_name = "notificacoes"

urlpatterns = [
    path('', views.notificacoes, name="notificacoes"),
    path('detalhe_notificacao/<int:id>/', views.detalhe_notificacao, name="detalhe_notificacao"),
    path('nova_notificacao/', views.nova_notificacao, name="nova_notificacao"),
]