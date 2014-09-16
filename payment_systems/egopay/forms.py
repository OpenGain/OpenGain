from django import forms
from .models import PSForUser
from payment_systems.forms import PSForUserDefaultForm


class PSForUserForm(PSForUserDefaultForm):
    class Meta:
        model = PSForUser
        fields = ('wallet',)

