from django.contrib import admin
from . models import Contrato, Item, Tipo, AditivoPrazo, AditivoValor, Supressao, Metafisico

admin.site.register(Contrato)
admin.site.register(Item)
admin.site.register(Tipo)
admin.site.register(AditivoPrazo)
admin.site.register(AditivoValor)
admin.site.register(Supressao)
admin.site.register(Metafisico)
