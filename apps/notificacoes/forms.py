from django.forms import ModelForm
from . models import Notificacoes


class NotificacoesForm(ModelForm):
    class Meta:
        model = Notificacoes
        fields = ['alert', 'title', 'text', 'icon', 'message_to', 'message_from']
