from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from apps.notificacoes.models import Notificacoes
from apps.juridico.models import Contrato
from . forms import ContratoForm


def juridico(request):
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    listar_contratos = Contrato.listar_contratos()
    return render(request, 'juridico/juridico.html', {
        'notificacoes_menu': notificacoes_menu,
        'qtd_notificacao': qtd_notificacao,
        'listar_contratos': listar_contratos,
    })


def item_contratos(request, id):
    return render(request, 'juridico/item_contratos.html')


def novo_contrato(request):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    form = ContratoForm(request.POST or None)
    if form.is_valid():
        formulario = form.save(commit=False)
        formulario.responsible = request.user
        formulario.save()
        return HttpResponseRedirect("/juridico/")
    return render(request, 'juridico/contrato_form.html',
                  {'form': form,
                   'qtd_notificacao': qtd_notificacao,
                   'notificacoes_menu': notificacoes_menu,
                   })
