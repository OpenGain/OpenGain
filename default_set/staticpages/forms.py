from django import forms
from django.conf import settings
from .models import StaticPage
from django.utils.translation import ugettext, ugettext_lazy as _


class StaticpageForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/\.~]+$',
                           help_text=_("Пример: '/about/contact/'. Убедитесь, что ввели начальную и конечную косые"
                                       " черты."),
                           error_message=_("Это значение должно содержать только буквы, цифры, точки,"
                                           " подчеркивания, тире, косые черты или тильды."))

    class Meta:
        model = StaticPage
        fields = '__all__'

    def clean_url(self):
        url = self.cleaned_data['url']
        if not url.startswith('/'):
            raise forms.ValidationError(
                _("В начале URL отсутствует косая черта."),
                code='missing_leading_slash',
            )
        if (settings.APPEND_SLASH and
                    'django.middleware.common.CommonMiddleware' in settings.MIDDLEWARE_CLASSES and
                not url.endswith('/')):
            raise forms.ValidationError(
                _("В конце URL отсутствует косая черта."),
                code='missing_trailing_slash',
            )
        return url

    def clean(self):
        url = self.cleaned_data.get('url', None)

        same_url = StaticPage.objects.filter(url=url)
        if self.instance.pk:
            same_url = same_url.exclude(pk=self.instance.pk)

        return super(StaticpageForm, self).clean()
