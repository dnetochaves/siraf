from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from apps.notificacoes.models import Notificacoes
from apps.juridico.models import Contrato, Item, Tipo, AditivoPrazo, AditivoValor, Supressao
from . forms import ContratoForm, ItemForm, TipoForm, AditivoPrazoForm, AditivoValorForm, SupressaoForm
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
        messages.success(request, 'Informa????o salva com sucesso')
        return HttpResponseRedirect("/juridico/item_contratos/" + str(item_contrato) + "/")
    return render(request, 'juridico/item_form.html',
                  {
                      'form': form,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })

# TODO Refazer o c??lculo  feito na view novo_aditivo_valor nessa  view tamb??m
# formulario.aditivo_value = valor_contrato + \  (valor_contrato * float(formulario.percentage) / 100)


def novo_item_aditivo_valor(request):
    id = request.POST['id_contract']
    id_aditivo = request.POST['id_aditivo']
    item1 = request.POST['item']
    item_description = request.POST['item_description']
    unit_price = request.POST['unit_price']
    amount = request.POST['amount']
    diferenca = request.POST['diferenca']
    total = float(unit_price.replace(',', '.')) * float(amount)

    contrato = get_object_or_404(Contrato, pk=id)
    valor_contrato = Item.valor_contrato(id)
    listar_item_id = Item.listar_item_id(id)
    if(valor_contrato == None):
        valor_contrato = 0
    valor_aditivo = AditivoValor.aditivo_value_id(id_aditivo)

    if(float(diferenca.replace(',', '.')) < float(total)):
        messages.error(
            request, 'O valor do item que voc?? est?? tentando adcionar ao aditivo ?? maior que o saldo restante')
    else:
        aditivo = get_object_or_404(AditivoValor, pk=id_aditivo)
        aditivo.difference = float(diferenca.replace(',', '.')) - total
        aditivo.save()

        Item.objects.create(
            item1=item1,
            item_description=item_description,
            unit_price=unit_price.replace(',', '.'),
            amount=amount,
            item_contrato=contrato,
            sum_value=float(unit_price.replace(',', '.')) *
            float(amount.replace(',', '.')),
            pos_aditivo_value=True,
            identity_aditivo_valor=id_aditivo,
        )

        messages.success(request, 'Item adcionado')

    return HttpResponseRedirect("/juridico/configurar_itens_aditivo/" + str(id) + "/" + str(id_aditivo) + "/")


def novo_item_supressao(request):
    id = request.POST['id_contract']
    id_supressao = request.POST['id_supressao']
    item1 = request.POST['item']
    item_description = request.POST['item_description']
    unit_price = request.POST['unit_price']
    amount = request.POST['amount']
    diferenca = request.POST['diferenca']
    total = float(unit_price.replace(',', '.')) * float(amount)

    contrato = get_object_or_404(Contrato, pk=id)
    valor_contrato = Item.valor_contrato(id)
    listar_item_id = Item.listar_item_id(id)
    if(valor_contrato == None):
        valor_contrato = 0
    supressao = Supressao.get_supressao(id_supressao)

    if(float(diferenca.replace(',', '.')) < float(total)):
        messages.error(
            request, 'O valor do item que voc?? est?? tentando adcionar ao aditivo ?? maior que o saldo restante')
    else:
        sup = get_object_or_404(Supressao, pk=id_supressao)
        sup.difference = float(diferenca.replace(',', '.')) - total
        sup.save()

        Item.objects.create(
            item1=item1,
            item_description=item_description,
            unit_price=unit_price.replace(',', '.'),
            amount=amount,
            item_contrato=contrato,
            sum_value=float(unit_price.replace(',', '.')) *
            float(amount.replace(',', '.')),
            pos_supressao=True,
            identity_supressao=id_supressao,
        )

        messages.success(request, 'Item adcionado')

    return HttpResponseRedirect("/juridico/configurar_itens_supressao/" + str(id) + "/" + str(id_supressao) + "/")


def excluir_item_aditivo_valor(request, id_contract, id_aditivo, id_item):
    item = get_object_or_404(Item, pk=id_item)
    aditivo = get_object_or_404(AditivoValor, pk=id_aditivo)
    aditivo.difference = aditivo.difference + item.sum_value
    aditivo.save()
    item.delete()

    adititvo_valor = get_object_or_404(AditivoValor, pk=id_aditivo)
    valor_contrato = Item.valor_contrato(id_contract)
    adititvo_valor.aditivo_value = valor_contrato + \
        (valor_contrato * float(adititvo_valor.percentage) / 100)
    # print(adititvo_valor.aditivo_value)

    adititvo_valor.save()
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
        messages.success(request, 'Informa????o salva com sucesso')
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
        messages.success(request, 'Informa????o salva com sucesso')
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
        messages.success(request, 'Informa????o salva com sucesso')
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
    listar_supressao_contract = Supressao.listar_supressao_contract(id)
    return render(request, 'juridico/dados_contrato.html',
                  {
                      'aditivo_por_contrato': aditivo_por_contrato,
                      'valor_contrato': valor_contrato,
                      'contrato': contrato,
                      'listar_item_id': listar_item_id,
                      'total_item_id': total_item_id,
                      'lista_aditivo_valor': lista_aditivo_valor,
                      'listar_supressao_contract': listar_supressao_contract,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                  })


def dados_aditivo_valor(request, id_contract, id_aditivo):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    aditivo_por_contrato = AditivoPrazo.aditivo_por_contrato(id_contract)
    valor_contrato = Item.valor_contrato(id_contract)
    contrato = Contrato.contrato_id(id_contract)
    listar_item_id = Item.listar_item_id(id_contract)
    total_item_id = Item.total_item_id(id_contract)
    lista_aditivo_valor = AditivoValor.aditivo_value_contract(id_contract)
    listar_identity_aditivo_valor = Item.listar_identity_aditivo_valor(
        id_aditivo)
    listar_supressao_contract = Supressao.listar_supressao_contract(
        id_contract)

    return render(request, 'juridico/dados_contrato.html',
                  {
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'aditivo_por_contrato': aditivo_por_contrato,
                      'valor_contrato': valor_contrato,
                      'contrato': contrato,
                      'listar_item_id': listar_identity_aditivo_valor,
                      'total_item_id': total_item_id,
                      'lista_aditivo_valor': lista_aditivo_valor,
                      'listar_identity_aditivo_valor': listar_identity_aditivo_valor,
                      'listar_supressao_contract': listar_supressao_contract,
                  })


def dados_supressao(request, id_contract, id_supressao):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    aditivo_por_contrato = AditivoPrazo.aditivo_por_contrato(id_contract)
    valor_contrato = Item.valor_contrato(id_contract)
    contrato = Contrato.contrato_id(id_contract)
    listar_item_id = Item.listar_item_id(id_contract)
    total_item_id = Item.total_item_id(id_contract)
    lista_aditivo_valor = AditivoValor.aditivo_value_contract(id_contract)
    listar_identity_supressao = Item.listar_identity_supressao(
        id_supressao)
    listar_supressao_contract = Supressao.listar_supressao_contract(
        id_contract)

    return render(request, 'juridico/dados_contrato.html',
                  {
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'aditivo_por_contrato': aditivo_por_contrato,
                      'valor_contrato': valor_contrato,
                      'contrato': contrato,
                      'listar_item_id': listar_identity_supressao,
                      'total_item_id': total_item_id,
                      'lista_aditivo_valor': lista_aditivo_valor,
                      'listar_identity_supressao': listar_identity_supressao,
                      'listar_supressao_contract': listar_supressao_contract,
                  })


def novo_tipo(request):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    form = TipoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Informa????o salva com sucesso')
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


def deletar_aditivo_valor(request, id):
    aditivo_valor = get_object_or_404(AditivoValor, pk=id)
    item = Item.objects.filter(identity_aditivo_valor=id)
    for itens in item:
        itens.delete()
    aditivo_valor.delete()
    messages.success(request, 'Aditivo de valor excluido com sucesso')
    return HttpResponseRedirect("/juridico/dados_contrato/" + str(aditivo_valor.contract.id) + "/")


def deletar_supressao(request, id):
    supressao = get_object_or_404(Supressao, pk=id)
    item = Item.objects.filter(identity_supressao=id)
    for itens in item:
        itens.delete()
    supressao.delete()
    messages.success(request, 'Supress??o excluido com sucesso')
    return HttpResponseRedirect("/juridico/dados_contrato/" + str(supressao.contract.id) + "/")


def novo_aditivo_valor(request, id):
    contrato = get_object_or_404(Contrato, pk=id)
    valor_contrato = Item.valor_contrato(id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)

    # TODO pega o valor total das porventagem de cada aditivo feito. Melhorar nome da variavel
    valor_percentage_contract = AditivoValor.valor_percentage_contract(id)

    form = AditivoValorForm(request.POST or None)
    if form.is_valid():
        formulario = form.save(commit=False)
        if(valor_percentage_contract == None):
            valor_percentage_contract = 0
        if(valor_percentage_contract + formulario.percentage <= 25):
            if(valor_contrato == None):
                valor_contrato = 0
                messages.error(
                    request, 'O cantrato que voc?? est?? tentando fazer uma aditivo de valor n??o possue itens cadastrados.')
                return HttpResponseRedirect("/juridico/listar_contratos/")
            formulario.contract = contrato

            # TODO Refatorar codigo (criar uma funcao separada)
            formulario.aditivo_value = valor_contrato + \
                (valor_contrato * float(formulario.percentage) / 100)

            formulario.difference = valor_contrato - valor_contrato + \
                (valor_contrato * float(formulario.percentage) / 100)

            data1 = formulario.signature_date + \
                relativedelta(months=+formulario.validity)
            formulario.end_validity = data1

            formulario.save()

            aditivo_valor = AditivoValor.aditivo_value_last()
            id_aditivo = aditivo_valor.id

            return HttpResponseRedirect("/juridico/configurar_itens_aditivo/" + str(id) + "/" + str(id_aditivo) + "/")
        else:
            a = 25 - valor_percentage_contract
            messages.info(request, 'Aten????o! Voc?? usou de um limite de 25%  ' +
                          str(valor_percentage_contract) + '%  e restam ' + str(a)+'%')

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
    listar_identity_aditivo_valor = Item.listar_identity_aditivo_valor(
        id_aditivo)
    listar_item_id_origin = Item.listar_item_id_origin(id)
    if(valor_contrato == None):
        valor_contrato = 0
    valor_aditivo = AditivoValor.aditivo_value_id(id_aditivo)
    diferenca = valor_aditivo.difference
    return render(request, 'juridico/configurar_itens_aditivo.html',
                  {
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'valor_contrato': valor_contrato,
                      'valor_aditivo': valor_aditivo,
                      'diferenca': diferenca,
                      'nome_contrato': contrato.company,
                      'listar_identity_aditivo_valor': listar_identity_aditivo_valor,
                      'listar_item_id_origin': listar_item_id_origin,
                      'id_contract': id,
                      'id_aditivo': id_aditivo,
                  })


def get_item_supressao(request, id, id_supressao, id_item):
    get_item = get_object_or_404(Item, pk=id_item)
    id_item_copy = get_item.id
    item_description_copy = get_item.item_description
    item_copy = get_item.item1
    unit_price_copy = get_item.unit_price
    amount_copy = get_item.amount
    item_contrato_copy = get_item.item_contrato
    sum_value_copy = get_item.sum_value
    sum_value_copy = get_item.sum_value
    contrato = get_object_or_404(Contrato, pk=id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    valor_contrato = Item.valor_contrato(id)
    supressao = Supressao.get_supressao(id_supressao)
    identity_supressao = Item.listar_identity_supressao(id_supressao)
    listar_item_id_origin = Item.listar_item_id_origin(id)
    if(valor_contrato == None):
        valor_contrato = 0
    #valor_aditivo = AditivoValor.aditivo_value_id(id_aditivo)

    #diferenca = valor_aditivo.difference
    return render(request, 'juridico/configurar_itens_supressao.html',
                  {
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'valor_contrato': valor_contrato,
                      'supressao': supressao,
                      'nome_contrato': contrato.company,
                      'identity_supressao': identity_supressao,
                      'listar_item_id_origin': listar_item_id_origin,
                      'id_contract': id,
                      'id_supressao': id_supressao,
                      'id_item_copy': id_item_copy,
                      'item_copy': item_copy,
                      'item_description_copy': item_description_copy,
                      'unit_price_copy': unit_price_copy,
                      'amount_copy': amount_copy,
                  })


def get_item(request, id, id_aditivo, id_item):
    get_item = get_object_or_404(Item, pk=id_item)
    id_item_copy = get_item.id
    item_description_copy = get_item.item_description
    item_copy = get_item.item1
    unit_price_copy = get_item.unit_price
    amount_copy = get_item.amount
    item_contrato_copy = get_item.item_contrato
    sum_value_copy = get_item.sum_value
    sum_value_copy = get_item.sum_value
    contrato = get_object_or_404(Contrato, pk=id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    valor_contrato = Item.valor_contrato(id)
    listar_identity_aditivo_valor = Item.listar_identity_aditivo_valor(
        id_aditivo)
    listar_item_id_origin = Item.listar_item_id_origin(id)
    if(valor_contrato == None):
        valor_contrato = 0
    valor_aditivo = AditivoValor.aditivo_value_id(id_aditivo)
    diferenca = valor_aditivo.difference
    return render(request, 'juridico/configurar_itens_aditivo.html',
                  {
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'valor_contrato': valor_contrato,
                      'valor_aditivo': valor_aditivo,
                      'diferenca': diferenca,
                      'nome_contrato': contrato.company,
                      'listar_identity_aditivo_valor': listar_identity_aditivo_valor,
                      'listar_item_id_origin': listar_item_id_origin,
                      'id_contract': id,
                      'id_aditivo': id_aditivo,
                      'id_item_copy': id_item_copy,
                      'item_copy': item_copy,
                      'item_description_copy': item_description_copy,
                      'unit_price_copy': unit_price_copy,
                      'amount_copy': amount_copy,
                  })


def processos(request, id_contract, company):
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    return render(request, 'juridico/processos.html',
                  {
                      'id_contract': id_contract,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'company': company
                  })


def nova_supressao(request, id):
    contrato = get_object_or_404(Contrato, pk=id)
    valor_contrato = Item.valor_contrato(id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)

    # TODO pega o valor total das porventagem de cada supressao feito. Melhorar nome da variavel
    valor_percentage_contract = Supressao.valor_percentage_contract_sup(id)
    print(valor_percentage_contract)
    form = SupressaoForm(request.POST or None)
    if form.is_valid():
        formulario = form.save(commit=False)

        if(valor_percentage_contract == None):
            valor_percentage_contract = 0
        if(valor_percentage_contract + formulario.percentage <= 25):
            if(valor_contrato == None):
                valor_contrato = 0
                messages.error(
                    request, 'O cantrato que voc?? est?? tentando fazer uma aditivo de valor n??o possue itens cadastrados.')
                return HttpResponseRedirect("/juridico/listar_contratos/")

            formulario.contract = contrato

            # TODO Refatorar codigo (criar uma funcao separada)
            formulario.aditivo_value = valor_contrato - \
            (valor_contrato * float(formulario.percentage) / 100)

            formulario.difference = valor_contrato - valor_contrato + \
                (valor_contrato * float(formulario.percentage) / 100)

            data1 = formulario.signature_date + \
                relativedelta(months=+formulario.validity)
            formulario.end_validity = data1

            formulario.save()

            supressao = Supressao.supressao_value_last()
            id_supressao = supressao.id

            return HttpResponseRedirect("/juridico/configurar_itens_supressao/" + str(id) + "/" + str(id_supressao) + "/")
        else:
            a = 25 - valor_percentage_contract
            messages.info(request, 'Aten????o! Voc?? usou de um limite de 25%  ' +
                          str(valor_percentage_contract) + '%  e restam ' + str(a)+'%')

    return render(request, 'juridico/supressao_form.html',
                  {
                      'form': form,
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'valor_contrato': valor_contrato,
                      'nome_contrato': contrato.company,
                  })


def configurar_itens_supressao(request, id, id_supressao):
    contrato = get_object_or_404(Contrato, pk=id)
    qtd_notificacao = Notificacoes.qtd_notificacoes(request.user.id)
    notificacoes_menu = Notificacoes.listar_notificacoes_menu(request.user.id)
    valor_contrato = Item.valor_contrato(id)
    supressao = Supressao.get_supressao(id_supressao)
    identity_supressao = Item.listar_identity_supressao(id_supressao)
    listar_item_id_origin = Item.listar_item_id_origin(id)
    if(valor_contrato == None):
        valor_contrato = 0
    listar_identity_supressao = Item.listar_identity_supressao(id_supressao)
    diferenca = supressao.difference
    return render(request, 'juridico/configurar_itens_supressao.html',
                  {
                      'qtd_notificacao': qtd_notificacao,
                      'notificacoes_menu': notificacoes_menu,
                      'valor_contrato': valor_contrato,
                      'supressao': supressao,
                      'diferenca': diferenca,
                      'nome_contrato': contrato.company,
                      'identity_supressao': identity_supressao,
                      'listar_item_id_origin': listar_item_id_origin,
                      'id_contract': id,
                      'id_supressao': id_supressao,
                      'listar_identity_supressao': listar_identity_supressao
                  })
