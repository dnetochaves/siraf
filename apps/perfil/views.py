from django.shortcuts import render
from apps.notificacoes.models import Notificacoes

# Create your views here.
def perfil(request):
    notificacoes = Notificacoes.listar_notificacoes_menu(request.user.id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    return render(request, 'perfil/perfil.html', {
        'notificacoes': notificacoes,
        'qtd_notificacao': qtd_notificacao
    })
