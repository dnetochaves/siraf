from django.forms import ModelForm
from . models import Contrato, Item


class ContratoForm(ModelForm):
    class Meta:
        model = Contrato
        fields = ['company', 'type', 'number', 'validity', 'signature_date']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item', 'item_description',
                  'unit_price', 'amount', 'item_contrato']
