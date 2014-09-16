from django import forms
from django.utils.translation import ugettext_lazy as _


class TicketForm(forms.Form):
    subject = forms.CharField(label=_('Тема'), max_length=100, required=True)
    text = forms.CharField(label=_('Сообщение'), max_length=500, required=True, widget=forms.Textarea)


class TicketMessageForm(forms.Form):
    message = forms.CharField(label=_('Сообщение'), max_length=500, required=True, widget=forms.Textarea)
