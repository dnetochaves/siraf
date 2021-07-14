from django.db import models
from django.contrib.auth.models import User


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
    
    def __str__(self):
        return self.title
