from django.forms import ModelForm
from . models import Contrato


class ContratoForm(ModelForm):
    class Meta:
        model = Contrato
        fields = ['company', 'type', 'number', 'validity']
