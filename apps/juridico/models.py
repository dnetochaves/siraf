from django.db import models
from django.contrib.auth.models import User


class Contrato(models.Model):
    company = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=True)
    number = models.IntegerField()
    validity = models.IntegerField()
    responsible = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="responsible")

    def listar_contratos():
        return Contrato.objects.all()

    def __str__(self):
        return self.company


class Item(models.Model):
    item = models.CharField(max_length=50, null=True, blank=True)
    item_description = models.CharField(max_length=100, null=True, blank=True)
    unit_price = models.FloatField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    item_contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.item
