from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from apps.notificacoes.models import Notificacoes
from apps.juridico.models import Contrato, Item, Tipo, AditivoPrazo, AditivoValor
from . forms import ContratoForm, ItemForm, TipoForm, AditivoPrazoForm, AditivoValorForm
from django.contrib import messages
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import datetime


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
    contrato = Contrato.contrato_id(id)
    request.session['session_id_contrato'] = id
    return render(request, 'juridico/item_contratos.html',
                  {
                      'notificacoes_menu': notificacoes_menu,
                      'qtd_notificacao': qtd_notificacao,
                      'listar_contratos': listar_contratos,
                      'listar_item_id': listar_item_id,
                      'valor_contrato': valor_contrato,
                      'contrato': contrato
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


def novo_item_aditivo_valor(request):
    id = request.POST['id_contract']
    id_aditivo = request.POST['id_aditivo']
    item = request.POST['item']
    item_description = request.POST['item_description']
    unit_price = request.POST['unit_price']
    amount = request.POST['amount']

    #print(f'id: {id}')
    #print(f'id_aditivo: {id_aditivo}')
    #print(f'item: {item}')
    #print(f'item_description: {item_description}')
    #print(f'unit_price: {unit_price}')
    #print(f'amount: {amount}')

    # formulario.sum_value = formulario.unit_price * formulario.amount

    contrato = get_object_or_404(Contrato, pk=id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    valor_contrato = Item.valor_contrato(id)
    listar_item_id = Item.listar_item_id(id)
    if(valor_contrato == None):
        valor_contrato = 0
    valor_aditivo = AditivoValor.aditivo_value_id(id_aditivo)
    diferenca = valor_aditivo.aditivo_value - valor_contrato

    Item.objects.create(
        item=item,
        item_description=item_description,
        unit_price=unit_price,
        amount=amount,
        item_contrato=contrato,
        sum_value=int(unit_price) * int(amount),
        pos_aditivo_value=True,
        identity_aditivo_valor=id_aditivo,
    )

    return render(request, 'juridico/configurar_itens_aditivo.html',
                  {
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'valor_contrato': valor_contrato,
                      'valor_aditivo': valor_aditivo,
                      'diferenca': diferenca,
                      'nome_contrato': contrato.company,
                      'listar_item_id': listar_item_id,
                      'id_contract': id,
                      'id_aditivo': id_aditivo,
                  })


def excluir_item_aditivo_valor(request, id_contract, id_aditivo, id_item):
    item = get_object_or_404(Item, pk=id_item)
    item.remove_sum = True
    item.pos_aditivo_value = True
    item.identity_aditivo_valor = id_aditivo
    item.save()
    return HttpResponseRedirect("/juridico/configurar_itens_aditivo/" + str(id_contract) + "/" + str(id_aditivo) + "/")


def novo_item_session(request, id):
    contrato = get_object_or_404(Contrato, pk=id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    form = ItemForm(request.POST or None)
    if form.is_valid():
        formulario = form.save(commit=False)
        formulario.item_contrato = contrato
        formulario.sum_value = formulario.unit_price * formulario.amount
        form.save()
        messages.success(request, 'Informação salva com sucesso')
        return HttpResponseRedirect("/juridico/item_contratos/" + str(id) + "/")
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
    contrato = get_object_or_404(
        Contrato, pk=request.session['session_id_contrato'])
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        formulario = form.save(commit=False)
        formulario.item_contrato = contrato
        formulario.sum_value = formulario.unit_price * formulario.amount
        form.save()
        return HttpResponseRedirect("/juridico/item_contratos/" + str(request.session['session_id_contrato']) + "/")
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
        data1 = six_months = formulario.signature_date + \
            relativedelta(months=+formulario.validity)
        # print(a)
        formulario.end_validity = data1
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


def novo_aditivo_prazo(request, id):
    contrato = get_object_or_404(Contrato, pk=id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    form = AditivoPrazoForm(request.POST or None)
    if form.is_valid():
        formulario = form.save(commit=False)
        formulario.contract = contrato
        data1 = six_months = formulario.signature_date + \
            relativedelta(months=+formulario.validity)
        formulario.end_validity = data1
        form.save()
        messages.success(request, 'Informação salva com sucesso')
        return HttpResponseRedirect("/juridico/listar_contratos/")
    return render(request, 'juridico/aditivo_prazo_form.html',
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
        formulario = form.save(commit=False)
        data1 = six_months = formulario.signature_date + \
            relativedelta(months=+formulario.validity)
        # print(a)
        formulario.end_validity = data1
        formulario.save()
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


def dados_contrato(request, id):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    aditivo_por_contrato = AditivoPrazo.aditivo_por_contrato(id)
    valor_contrato = Item.valor_contrato(id)
    contrato = Contrato.contrato_id(id)
    listar_item_id = Item.listar_item_id(id)
    total_item_id = Item.total_item_id(id)
    lista_aditivo_valor = AditivoValor.aditivo_value_contract(id)
    return render(request, 'juridico/dados_contrato.html',
                  {
                      'aditivo_por_contrato': aditivo_por_contrato,
                      'valor_contrato': valor_contrato,
                      'contrato': contrato,
                      'listar_item_id': listar_item_id,
                      'total_item_id': total_item_id,
                      'lista_aditivo_valor': lista_aditivo_valor,
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


def deletar_aditivo_praso(request, id):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    aditivo_prazo = get_object_or_404(AditivoPrazo, pk=id)
    aditivo_prazo.delete()
    return HttpResponseRedirect("/juridico/dados_contrato/" + str(aditivo_prazo.contract.id) + "/",
                                {
        'qtd_notificacao': qtd_notificacao,
        'notificacoes_menu': notificacoes_menu,
    })


def novo_aditivo_valor(request, id):
    contrato = get_object_or_404(Contrato, pk=id)
    valor_contrato = Item.valor_contrato(id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    valor_percentage_contract = AditivoValor.valor_percentage_contract(id)
    form = AditivoValorForm(request.POST or None)
    if form.is_valid():
        formulario = form.save(commit=False)
        if(valor_percentage_contract == None):
            valor_percentage_contract = 0
        if(valor_percentage_contract + formulario.percentage <= 25):
            formulario.contract = contrato
            if(valor_contrato == None):
                valor_contrato = 0
                messages.error(
                    request, 'O cantrato que você está tentando fazer uma aditivo de valor não possue itens cadastrados.')
                return HttpResponseRedirect("/juridico/listar_contratos/")
            formulario.aditivo_value = valor_contrato + \
                (valor_contrato * float(formulario.percentage) / 100)
            data1 = six_months = formulario.signature_date + \
                relativedelta(months=+formulario.validity)
            formulario.end_validity = data1
            formulario.save()
            aditivo_valor = AditivoValor.aditivo_value_last()
            id_aditivo = aditivo_valor.id
            return HttpResponseRedirect("/juridico/configurar_itens_aditivo/" + str(id) + "/" + str(id_aditivo) + "/")
        else:
            a = 25 - valor_percentage_contract
            messages.error(request, 'Desculpa! Você usou de um limite de 25%  ' +
                           str(valor_percentage_contract) + '  e restam ' + str(a))

    return render(request, 'juridico/aditivo_valor_form.html',
                  {
                      'form': form,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'valor_contrato': valor_contrato,
                      'nome_contrato': contrato.company,
                      'valor_percentage_contract': valor_percentage_contract,
                  })


def configurar_itens_aditivo(request, id, id_aditivo):
    contrato = get_object_or_404(Contrato, pk=id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    valor_contrato = Item.valor_contrato(id)
    listar_item_id = Item.listar_item_id(id)
    if(valor_contrato == None):
        valor_contrato = 0
    valor_aditivo = AditivoValor.aditivo_value_id(id_aditivo)
    diferenca = valor_aditivo.aditivo_value - valor_contrato
    return render(request, 'juridico/configurar_itens_aditivo.html',
                  {
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'valor_contrato': valor_contrato,
                      'valor_aditivo': valor_aditivo,
                      'diferenca': diferenca,
                      'nome_contrato': contrato.company,
                      'listar_item_id': listar_item_id,
                      'id_contract': id,
                      'id_aditivo': id_aditivo,
                  })
