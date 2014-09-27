from django import forms
from django.contrib import admin
from main import opengain_admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from main.discovers import PAYMENT_SYSTEMS
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin

def get_ps_inlines():
    retval = []
    for ps in PAYMENT_SYSTEMS:
        module = import_module('payment_systems.' + ps.NAME + '.admin')
        inline_class = getattr(module, 'PSForUserInline')
        retval.append(inline_class)
    return retval


def get_ps_list_display():
    retval = []
    for ps in PAYMENT_SYSTEMS:
        retval.append(ps.NAME)
    return tuple(retval)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Еще раз', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли разные")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'date_joined', 'last_login', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]


@admin.register(UserProfile, site=opengain_admin)
class UserProfileAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
                       'date_joined', 'username', 'email', 'sponsor', 'lang', ) + get_ps_list_display()
    list_filter = ('is_active', )
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'sponsor', )}),
        (_('Даты'), {'fields': ('date_joined', 'last_login', 'timezone')}),
        (_('Чеки'), {'fields': ('is_active', 'is_superuser', 'is_alerts_referrals',
                                'is_alerts_comission', 'is_alerts_other')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'sponsor')}
        ),
    )
    raw_id_fields = ('sponsor',)
    search_fields = (
        'username', 'email', 'sponsor__username', 'sponsor__email')
    ordering = ('-id', 'username', 'email',)
    filter_horizontal = ()
    inlines = get_ps_inlines()


@admin.register(Transaction, site=opengain_admin)
class TransactionAdmin(admin.ModelAdmin):
    def withdraw(self, request, queryset):
        for tr in queryset:
            module = import_module('payment_systems.' + tr.ps + '.views')
            withdraw_method = getattr(module, 'transaction_withdraw')
            try:
                withdraw_method(tr)
            except Exception as e:
                self.message_user(request, _('Error: %s') % e)

    withdraw.short_description = _('Обработать вывод')

    list_display = (
        'created', 'user', 'other_user', 'ps', 'amount', 'transaction_type', 'balance_before', 'balance_after', 'batch',
        'is_ended')
    list_filter = ('is_ended', 'ps', 'transaction_type', )
    search_fields = ('user__username', 'user__email', 'other_user__username', 'other_user__email')
    ordering = ('-id',)
    raw_id_fields = ('user', 'other_user', )
    actions = (withdraw,)


@admin.register(Plan, site=opengain_admin)
class PlanAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'min_amount', 'max_amount', 'percent', 'period')


