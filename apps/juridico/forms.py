from django.forms import ModelForm
from . models import Contrato, Item, Tipo, AditivoPrazo, AditivoValor


class ContratoForm(ModelForm):
    class Meta:
        model = Contrato
        fields = ['company', 'number', 'validity',
                  'signature_date', 'type_contrato', 'official_diary']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item1', 'item_description',
                  'unit_price', 'amount', 'item_contrato']


class TipoForm(ModelForm):
    class Meta:
        model = Tipo
        fields = ['name', 'description']


class AditivoPrazoForm(ModelForm):
    class Meta:
        model = AditivoPrazo
        fields = ['signature_date', 'validity',
                  'signature_date', 'official_diary']


class AditivoValorForm(ModelForm):
    class Meta:
        model = AditivoValor
        fields = ['signature_date', 'validity', 'official_diary', 'percentage']
