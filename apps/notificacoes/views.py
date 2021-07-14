from django.shortcuts import render
from . models import Notificacoes


def notificacoes(request):
    notificacoes = Notificacoes.listar_notificacoes(request.user.id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    return render(request, 'notificacoes/notificacoes.html', {
        'notificacoes': notificacoes,
        'qtd_notificacao': qtd_notificacao
    })


def detalhe_notificacao(request, id):
    notificacoes = Notificacoes.listar_notificacoes(request.user.id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    detalhe_notificacoes = Notificacoes.detalhe_notificacao(id)
    return render(request, 'notificacoes/detalhe_notificacoes.html', {
        'notificacoes': notificacoes,
        'qtd_notificacao': qtd_notificacao,
        'detalhe_notificacoes': detalhe_notificacoes
    })
