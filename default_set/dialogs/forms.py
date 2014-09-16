from django import forms
from default_set.models import UserProfile
from django.utils.translation import ugettext_lazy as _


class DialogForm(forms.Form):
    user = forms.CharField(label=_('Получатель'), max_length=100, required=True)
    message = forms.CharField(label=_('Сообщение'), max_length=500, required=True, widget=forms.Textarea)

    def __init__(self, user=None, *args, **kwargs):
        super(DialogForm, self).__init__(*args, **kwargs)
        self._user = user

    def clean_user(self):
        user = self.cleaned_data["user"]
        try:
            u = UserProfile.objects.get(username__iexact=user)
            self.recipient = u
        except UserProfile.DoesNotExist:
            raise forms.ValidationError(_('Пользователь с таким логином не зарегистрирован'))
        if u.is_superuser:
            raise forms.ValidationError(_('Чтобы написать администрации проекта - создайте тикет'))
        if u == self._user:
            raise forms.ValidationError(_('Вы не можете отправить сообщение самому себе'))
        return user


class DialogMessageForm(forms.Form):
    message = forms.CharField(label=_('Сообщение'), max_length=500, required=True, widget=forms.Textarea)
