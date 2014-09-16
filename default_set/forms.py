from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from default_set.models import UserProfile
from pytz import common_timezones
from django.utils.translation import ugettext_lazy as _
from decimal import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template import loader
from django.conf import settings
from main import discovers
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    timezone = forms.ChoiceField(choices=[(x, x) for x in common_timezones], initial='UTC', label=_('Часовой пояс'))
    sponsor_username = forms.CharField(max_length=45, label=_('Вас пригласил'))

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            UserProfile.objects.get(username__iexact=username)
        except UserProfile.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_sponsor_username(self):
        sponsor_username = self.cleaned_data["sponsor_username"]
        try:
            UserProfile.objects.get(username__iexact=sponsor_username)
            return sponsor_username
        except UserProfile.DoesNotExist:
            return UserProfile.objects.get_main_admin().username


class SignInForm(AuthenticationForm):
    username = forms.CharField(max_length=45, label=_('Логин или Email'))

    error_messages = {
        'invalid_login': _("Пожалуйста, введите корректное имя пользователя (или Email) и пароль."),
        'inactive': _("Этот аккаунт заблокирован."),
    }

    # def __init__(self, *args, **kwargs):
    # ha = None
    #     if "hacking_attempts" in kwargs:
    #         ha = kwargs.pop("hacking_attempts")
    #     super(SignInForm, self).__init__(*args, **kwargs)
    #     if ha:
    #         self.fields["captcha"] = ReCaptchaField(label=u'Введите код с картинки')


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user_exist = False
            self.user_cache = None

            if '@' in username:
                try:
                    user = UserProfile.objects.get(email__iexact=username)
                    username = user.username
                    user_exist = True
                except UserProfile.DoesNotExist:
                    pass
            else:
                try:
                    user = UserProfile.objects.get(username__iexact=username)
                    username = user.username
                    user_exist = True
                except UserProfile.DoesNotExist:
                    pass

            if user_exist:
                self.user_cache = authenticate(username=username,
                                               password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CustomPasswordResetForm(forms.Form):
    username_or_email = forms.CharField(label=_("Логин или Email"), max_length=45)

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data["username_or_email"]

        email = None
        if '@' in username_or_email:
            try:
                user = UserProfile.objects.get(email__iexact=username_or_email)
                email = user.email
            except UserProfile.DoesNotExist:
                pass
        else:
            try:
                user = UserProfile.objects.get(username__iexact=username_or_email)
                email = user.email
            except UserProfile.DoesNotExist:
                pass

        if not email:
            raise forms.ValidationError(_('Пользователь с таким логином или Email-адресом не зарегистрирован'))

        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail

        UserModel = UserProfile
        email = self.cleaned_data["username_or_email"]

        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)

            if html_email_template_name:
                html_email = loader.render_to_string(html_email_template_name, c)
            else:
                html_email = None
            send_mail(subject, email, from_email, [user.email], html_message=html_email)


class WithdrawForm(forms.Form):
    ps = forms.ChoiceField(label=_('Платежная система'), choices=discovers.PAYMENT_SYSTEMS_TUPLE, required=True)
    amount = forms.DecimalField(label=_('Сумма'), min_value=settings.WITHDRAWAL_MIN, max_value=settings.WITHDRAWAL_MAX,
                                max_digits=8,
                                decimal_places=2, initial=0.00, required=True)


class DepositForm(forms.Form):
    ps = forms.ChoiceField(label=_('Платежная система'), choices=discovers.PAYMENT_SYSTEMS_TUPLE, required=True)
    amount = forms.DecimalField(label=_('Сумма'), min_value=settings.DEPOSIT_MIN, max_value=settings.DEPOSIT_MAX,
                                max_digits=8,
                                decimal_places=2, initial=10.00, required=True)


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('timezone', 'is_alerts_referrals',
                  'is_alerts_comission', 'is_alerts_other')


class TransferForm(forms.Form):
    username = forms.RegexField(label=_('Получатель'), max_length=30, required=True, regex=r'^[\w.@+-]+$',
                                error_messages={
                                    'invalid': _("Это значение может состоять из букв, цифр и знаков "
                                                 "@/./+/-/_.")})
    ps = forms.ChoiceField(label=_('Платежная система'), choices=discovers.PAYMENT_SYSTEMS_TUPLE, required=True)
    amount = forms.DecimalField(label=_('Сумма'), min_value=Decimal('0.1'), max_value=Decimal('100000'), max_digits=8,
                                decimal_places=2, initial=0.00, required=True)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            UserProfile.objects.get(username__iexact=username)
        except UserProfile.DoesNotExist:
            raise forms.ValidationError(_('Пользователь с таким логином не зарегистрирован'))
        return username


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=_("Старый пароль"),
                                   widget=forms.PasswordInput)
    password1 = forms.CharField(label=_("Новый пароль"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Подтверждение нового пароля"),
                                widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
