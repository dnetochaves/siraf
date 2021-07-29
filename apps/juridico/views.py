from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from apps.notificacoes.models import Notificacoes
from apps.juridico.models import Contrato, Item, Tipo
from . forms import ContratoForm, ItemForm, TipoForm
from django.contrib import messages


def juridico(request):
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    listar_contratos = Contrato.listar_contratos()
    listar_item = Item.listar_item()
    return render(request, 'juridico/juridico.html', {
        'notificacoes_menu': notificacoes_menu,
        'qtd_notificacao': qtd_notificacao,
        'listar_contratos': listar_contratos,
        'listar_item': listar_item,
    })


def item_contratos(request, id):
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    listar_contratos = Contrato.listar_contratos()
    listar_item_id = Item.listar_item_id(id)
    valor_contrato = Item.valor_contrato(id)
    return render(request, 'juridico/item_contratos.html',
                  {
                      'notificacoes_menu': notificacoes_menu,
                      'qtd_notificacao': qtd_notificacao,
                      'listar_contratos': listar_contratos,
                      'listar_item_id': listar_item_id,
                      'valor_contrato': valor_contrato
                  })


def novo_item(request):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    form = ItemForm(request.POST or None)
    if form.is_valid():
        item_contrato = request.POST['item_contrato']
        formulario = form.save(commit=False)
        formulario.sum_value = formulario.unit_price * formulario.amount
        form.save()
        messages.success(request, 'Informação salva com sucesso')
        return HttpResponseRedirect("/juridico/item_contratos/" + str(item_contrato) + "/")
    return render(request, 'juridico/item_form.html',
                  {
                      'form': form,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })


def editar_item(request, id):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    item = get_object_or_404(Item, pk=id)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        formulario = form.save(commit=False)
        formulario.sum_value = formulario.unit_price * formulario.amount
        form.save()
        # return HttpResponseRedirect("/juridico/item_form.html")
        return render(request, 'juridico/item_form.html', {'form': form})
    return render(request, 'juridico/item_form.html',
                  {
                      'form': form,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })


def deletar_item(request, id):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    item = get_object_or_404(Item, pk=id)
    form = ItemForm(request.POST or None, instance=item)
    if request.method == 'POST':
        item.delete()
        return HttpResponseRedirect("/juridico/item_contratos/" + str(item.item_contrato.id) + "/")
    return render(request, 'juridico/item_delete_confirm.html',
                  {
                      'item': item,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })


def novo_contrato(request):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    form = ContratoForm(request.POST or None)
    if form.is_valid():
        formulario = form.save(commit=False)
        formulario.responsible = request.user
        formulario.save()
        messages.success(request, 'Informação salva com sucesso')
        # return HttpResponseRedirect("/juridico/")
        form = ContratoForm()
        return render(request, 'juridico/contrato_form.html',
                      {
                          'form': form,
                          'qtd_notificacao': qtd_notificacao,
                          'notificacoes_menu': notificacoes_menu,
                      })
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


def novo_tipo(request):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    form = TipoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Informação salva com sucesso')
        return HttpResponseRedirect("/juridico/listar_tipos/")
    return render(request, 'juridico/tipo_form.html',
                  {
                      'form': form,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })


def listar_tipos(request):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    listar_tipos = Tipo.listar_tipo()
    return render(request, 'juridico/listar_tipos.html',
                  {
                      'listar_tipos': listar_tipos,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })


def editar_tipo(request, id):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    tipo = get_object_or_404(Tipo, pk=id)
    form = TipoForm(request.POST or None, instance=tipo)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/juridico/listar_tipos/")
        # return render(request, 'juridico/item_form.html', {'form': form})
    return render(request, 'juridico/tipo_form.html',
                  {
                      'form': form,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })


def deletar_tipo(request, id):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    tipo = get_object_or_404(Tipo, pk=id)
    form = TipoForm(request.POST or None, instance=tipo)
    if request.method == 'POST':
        tipo.delete()
        return HttpResponseRedirect("/juridico/listar_tipos/")
    return render(request, 'juridico/tipo_delete_confirm.html',
                  {
                      'form': form,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })
