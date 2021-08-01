from django import template
from apps.juridico.models import Contrato, Item, Tipo, AditivoPrazo

register = template.Library()


@register.filter()
def soma(val1, val2):
    return 'R$ ' + str(val1 * val2)


@register.filter()
def verificar_aditivo_prazo(id):
    vs = AditivoPrazo.aditivo_por_contrato(id)
    if(vs != ""):
        for v in vs:
            return 'sim' 
        return 'não'
    
