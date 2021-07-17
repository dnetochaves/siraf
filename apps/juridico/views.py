from django.shortcuts import render, redirect, get_object_or_404
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
                  {
                      'form': form,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })


def editar_contrato(request, id):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    contrato = get_object_or_404(Contrato, pk=id)
    form = ContratoForm(request.POST or None, instance=contrato)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/juridico/listar_contratos/")
    return render(request, 'juridico/contrato_form.html',
                  {
                      'form': form,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })


def deletar_contrato(request, id):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    contrato = get_object_or_404(Contrato, pk=id)
    form = ContratoForm(request.POST or None, instance=contrato)
    if request.method == 'POST':
        contrato.delete()
        return HttpResponseRedirect("/juridico/listar_contratos/")
    return render(request, 'juridico/contrato_delete_confirm.html',
                  {
                      'contrato': contrato,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })


def listar_contratos(request):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    listar_contratos = Contrato.listar_contratos()
    return render(request, 'juridico/listar_contratos.html',
                  {
                      'listar_contratos': listar_contratos,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })
