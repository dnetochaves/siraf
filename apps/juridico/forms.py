from django.forms import ModelForm
from . models import Contrato, Item, Tipo, AditivoPrazo


class ContratoForm(ModelForm):
    class Meta:
        model = Contrato
        fields = ['company', 'number', 'validity',
                  'signature_date', 'type_contrato']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item', 'item_description',
                  'unit_price', 'amount', 'item_contrato']


class TipoForm(ModelForm):
    class Meta:
        model = Tipo
        fields = ['name', 'description']

class AditivoPrazoForm(ModelForm):
    class Meta:
        model = AditivoPrazo
        fields = ['signature_date', 'validity', ]
