from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Avg


class Notificacoes(models.Model):
    ALERT_CHOICES = (
        ("d", "urgente"),
        ("s", "normal"),
        ("w", "atenção")
    )
    alert = models.CharField(
        max_length=1, choices=ALERT_CHOICES, blank=False, null=False)
    title = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True)
    icon = models.CharField(max_length=50, null=True, blank=True)
    message_to = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='message_to')
    message_from = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='message_from')

    def listar_notificacoes(id):
        return Notificacoes.objects.filter(message_from=id)

    def detalhe_notificacao(id):
        return Notificacoes.objects.filter(id=id)

    def listar_notificacoes_menu(id):
        return Notificacoes.objects.filter(message_from=id).order_by('-pk')[:4]

    def qtd_notificacoes(id):
        return Notificacoes.objects.filter(message_from=id).aggregate(Count('id'))['id__count']

    def __str__(self):
        return self.title
