from django.db import models


class Contrato(models.Model):
    company = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=True)
    number = models.IntegerField()
    validity = models.IntegerField()
