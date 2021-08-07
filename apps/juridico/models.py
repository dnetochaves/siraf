from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count


class Tipo(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def listar_tipo():
        return Tipo.objects.all()

    def __str__(self):
        return self.name


class Contrato(models.Model):
    company = models.CharField(max_length=50)
    type = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(auto_now=False, auto_now_add=True)
    number = models.CharField(max_length=50, blank=True, null=True)
    validity = models.IntegerField(blank=True, null=True)
    responsible = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="responsible")
    signature_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    type_contrato = models.ForeignKey(
        Tipo, on_delete=models.PROTECT, null=True, blank=True)
    end_validity = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    official_diary = models.CharField(max_length=50, blank=True, null=True)

    def listar_contratos():
        return Contrato.objects.all()
    
    def contrato_id(id):
        return Contrato.objects.get(pk=id)

    def __str__(self):
        return self.company


class Item(models.Model):
    item = models.CharField(max_length=50, null=True, blank=True)
    item_description = models.TextField(null=True, blank=True)
    unit_price = models.FloatField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    item_contrato = models.ForeignKey(
        Contrato, on_delete=models.CASCADE, null=True, blank=True)
    sum_value = models.FloatField(null=True, blank=True)
    sum_value1 = models.FloatField(null=True, blank=True)

    def listar_item():
        return Item.objects.all()

    def listar_item_id(id):
        return Item.objects.filter(item_contrato=id)

    def valor_contrato(id_contrato):
        return Item.objects.filter(item_contrato=id_contrato).aggregate(Sum('sum_value'))['sum_value__sum']
    
    def total_item_id(id):
        return Item.objects.filter(item_contrato=id).aggregate(Count('item'))['item__count']

    def __str__(self):
        return self.item


class AditivoPrazo(models.Model):
    contract = models.ForeignKey(Contrato, on_delete=models.CASCADE, blank=True, null=True)
    signature_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    validity = models.IntegerField(blank=True, null=True)
    end_validity = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    official_diary = models.CharField(max_length=50, blank=True, null=True)

    def listar_aditivo_prazo_contrato(id):
        return AditivoPrazo.objects.filter(contract=id)
    
    def aditivo_por_contrato(id):
        return AditivoPrazo.objects.filter(contract=id)

    def __str__(self):
        return str(self.contract)