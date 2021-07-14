from django.urls import path
from . import views

app_name = "notificacoes"

urlpatterns = [
    path('', views.notificacoes, name="notificacoes"),
]