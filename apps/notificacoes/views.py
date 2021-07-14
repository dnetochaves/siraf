from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . models import Notificacoes
from .forms import NotificacoesForm


def notificacoes(request):
    notificacoes = Notificacoes.listar_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    return render(request, 'notificacoes/notificacoes.html', {
        'notificacoes': notificacoes,
        'notificacoes_menu': notificacoes_menu,
        'qtd_notificacao': qtd_notificacao
    })


def detalhe_notificacao(request, id):
    notificacoes = Notificacoes.listar_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    detalhe_notificacoes = Notificacoes.detalhe_notificacao(id)
    return render(request, 'notificacoes/detalhe_notificacoes.html', {
        'notificacoes': notificacoes,
        'notificacoes_menu': notificacoes_menu,
        'qtd_notificacao': qtd_notificacao,
        'detalhe_notificacoes': detalhe_notificacoes
    })


def nova_notificacao(request):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    form = NotificacoesForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/notificacoes/")
    return render(request, 'notificacoes/notificacoes_form.html', 
    {'form': form, 
    'qtd_notificacao': qtd_notificacao,
    'notificacoes_menu': notificacoes_menu,
    })
