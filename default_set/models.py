from importlib import import_module
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Sum, Q
from django.http import Http404
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from pytz import common_timezones
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re
from default_set.dialogs.models import Dialog
from main import discovers
from main.discovers import PAYMENT_SYSTEMS_TUPLE
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django.utils import translation


class InsufficientBalance(Exception):
    def __str__(self):
        return _('Недостаточно средств')


class UserProfileManager(BaseUserManager):
    def _create_user(self, username, email, password,
                     is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('Имя пользователя должно быть установлено'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True,
                                 **extra_fields)

    def get_user_by_b64username(self, b64username):
        try:
            return self.get(username=urlsafe_base64_decode(force_text(b64username)))
        except:
            raise Http404

    def get_main_admin(self):
        return self.filter(is_superuser=True).order_by('pk')[0]


class UserProfile(AbstractBaseUser):
    username = models.CharField(_('Логин'), max_length=20, unique=True, db_index=True)
    email = models.EmailField(_('Email'), blank=False, null=False, default=None, unique=True, db_index=True)
    date_joined = models.DateTimeField(_('Регистрация'), default=timezone.now)
    timezone = models.CharField(_('Часовой пояс'), max_length=20, choices=[(x, x) for x in common_timezones],
                                default='UTC')
    is_superuser = models.BooleanField(_('Админ'), default=False)
    is_active = models.BooleanField(_('Активный'), default=True, db_index=True)
    is_alerts_referrals = models.BooleanField(_('Уведомления о новых рефералах'), default=True, db_index=True)
    is_alerts_comission = models.BooleanField(_('Уведомления о реферальной комиссии'), default=True, db_index=True)
    is_alerts_other = models.BooleanField(_('Другие уведомления'), default=True, db_index=True)
    sponsor = models.ForeignKey('self', verbose_name=_('Спонсор'), null=True, blank=True, db_index=True, default=None,
                                related_name='referrals')
    lang = models.CharField(_('Язык'), max_length=2, null=False, blank=False, default=settings.LANGUAGE_CODE,
                            choices=settings.LANGUAGES)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserProfileManager()

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return self.username

    def email_user(self, subject, email_template_name, context={}):
        context['site_domain'] = settings.PROJECT_DOMAIN
        context['site_name'] = settings.PROJECT_TITLE
        context['user'] = self
        current_lang = translation.get_language()
        translation.activate(self.lang)
        message = loader.render_to_string(email_template_name, context)
        send_mail(subject=subject, message='', html_message=message, recipient_list=[self.email],
                  from_email=settings.DEFAULT_FROM_EMAIL)
        translation.activate(current_lang)

    def get_full_name(self):
        return '{} <{}>'.format(self.username, self.email)

    def get_short_name(self):
        return self.username


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    def get_ps_class(self, ps):
        module = import_module('payment_systems.' + ps + '.models')
        return getattr(module, 'PSForUser')

    def get_ps_instance(self, ps):
        try:
            instance = getattr(self, ps)
        except ObjectDoesNotExist:
            instance = self.get_ps_class(ps).objects.create(user=self)
        return instance

    def get_ps_account(self, ps):
        return self.get_ps_instance(ps).wallet

    def get_ps_balance(self, ps):
        return self.get_ps_instance(ps).balance

    def get_ps_instances(self):
        retval = []
        for ps in PAYMENT_SYSTEMS_TUPLE:
            retval.append(self.get_ps_instance(ps[0]))
        return retval

    def get_balances_display(self):
        retval = []
        for ps in PAYMENT_SYSTEMS_TUPLE:
            retval.append((ps[1], self.get_ps_balance(ps[0])))
        return tuple(retval)

    def get_b64username(self):
        return force_text(urlsafe_base64_encode(force_bytes(self.username)))

    def get_dialog_by_user(self, user):
        dialogs = self.dialogs.select_related().filter(users=user)
        if not dialogs:
            dialog = Dialog.objects.create()
            dialog.users.add(self, user)
            return dialog
        return dialogs[0]

    def get_referrals_by_level(self, level):
        arg = 'sponsor' + ('__sponsor' * (level - 1))
        return UserProfile.objects.filter(**{arg: self})

    def get_my_referrals(self):
        return self.get_referrals_by_level(1)

    def get_all_referrals(self):
        retval = None
        for level in range(len(settings.REFERRAL_COMISSIONS)):
            referrals = self.get_referrals_by_level(level)
            if not retval:
                retval = referrals
            else:
                retval |= referrals
        return retval.order_by('-pk')

    def get_sponsor_level(self, sponsor):
        temp_sponsor = self.sponsor
        for level in range(len(settings.REFERRAL_COMISSIONS)):
            if temp_sponsor == sponsor:
                return level + 1
            temp_sponsor = getattr(temp_sponsor, 'sponsor')
        return 0

    def get_sponsors_and_percents(self):
        retval = ()
        temp_sponsor = self
        for percent in settings.REFERRAL_COMISSIONS:
            if temp_sponsor:
                temp_sponsor = temp_sponsor.sponsor
                if temp_sponsor: retval += ((temp_sponsor, percent),)
        return retval


TRANSACTION_DEPOSIT = 1
TRANSACTION_WITHDRAW = 2
TRANSACTION_TRANSFER_OUTGOING = 3
TRANSACTION_TRANSFER_INCOMING = 4
TRANSACTION_REFERRAL = 5
TRANSACTION_ACCRUAL = 6
TRANSACTION_ADMIN_SALARY = 7

TRANSACTION_TYPES = (
    (TRANSACTION_DEPOSIT, _('Пополнение баланса')),
    (TRANSACTION_WITHDRAW, _('Вывод средств')),
    (TRANSACTION_TRANSFER_OUTGOING, _('Внутренний перевод исходящий')),
    (TRANSACTION_TRANSFER_INCOMING, _('Внутренний перевод входящий')),
    (TRANSACTION_REFERRAL, _('Реферальная комиссия')),
    (TRANSACTION_ACCRUAL, _('Начисление процентов')),
    (TRANSACTION_ADMIN_SALARY, _('ЗП Админа')),
)


class TransactionManager(BaseUserManager):
    def get_deposits(self):
        return self.filter(transaction_type=TRANSACTION_DEPOSIT, is_ended=True)

    def get_deposits_amount(self):
        return self.get_deposits().aggregate(Sum('amount'))['amount__sum'] or 0

    def get_withdraws(self):
        return self.filter(transaction_type=TRANSACTION_WITHDRAW)

    def get_withdraws_amount(self):
        return abs(self.get_withdraws().aggregate(Sum('amount'))['amount__sum'] or 0)

    def get_transfers_incoming(self):
        return self.filter(transaction_type=TRANSACTION_TRANSFER_INCOMING, is_ended=True)

    def get_transfers_incoming_amount(self):
        return self.get_transfers_incoming().aggregate(Sum('amount'))['amount__sum'] or 0

    def get_transfers_outgoing(self):
        return self.filter(transaction_type=TRANSACTION_TRANSFER_OUTGOING, is_ended=True)

    def get_transfers_outgoing_amount(self):
        return abs(self.get_transfers_outgoing().aggregate(Sum('amount'))['amount__sum'] or 0)

    def get_referral_comissions(self):
        return self.filter(transaction_type=TRANSACTION_REFERRAL, is_ended=True)

    def get_referral_comissions_amount(self):
        return self.get_referral_comissions().aggregate(Sum('amount'))['amount__sum'] or 0

    def get_earnings(self):
        return self.filter(transaction_type=TRANSACTION_ACCRUAL, is_ended=True)

    def get_earnings_amount(self):
        return self.get_earnings().aggregate(Sum('amount'))['amount__sum'] or 0


class Transaction(models.Model):
    created = models.DateTimeField(_('Создание'), auto_now=False, auto_now_add=True, null=False, blank=False,
                                   default=timezone.now)
    last_update = models.DateTimeField(_('Изменение'), auto_now=True, auto_now_add=True, null=False, blank=False,
                                       default=timezone.now)
    user = models.ForeignKey(UserProfile, related_name='transactions', verbose_name=_('Пользователь'), null=True,
                             blank=False, db_index=True)
    ps = models.CharField(_('Платежка'), max_length=20, choices=discovers.PAYMENT_SYSTEMS_TUPLE, null=True, blank=False,
                          db_index=True)
    amount = models.DecimalField(_('Сумма'), max_digits=8, decimal_places=2, default=0, null=False, blank=False)
    transaction_type = models.IntegerField(_('Тип транзакции'), blank=False, null=True, db_index=True,
                                           choices=TRANSACTION_TYPES)
    balance_before = models.DecimalField(_('Баланс до'), max_digits=8, decimal_places=2, default=0, null=False,
                                         blank=False)
    balance_after = models.DecimalField(_('Баланс после'), max_digits=8, decimal_places=2, default=0, null=False,
                                        blank=False)
    batch = models.CharField(_('Батч'), max_length=50, null=True, blank=True, default=None)
    is_ended = models.BooleanField(_('Завершено'), default=False, db_index=True)
    other_user = models.ForeignKey(UserProfile, related_name='other_transactions',
                                   verbose_name=_('Второй пользователь'),
                                   null=True, blank=True)

    objects = TransactionManager()

    class Meta:
        ordering = ('-pk',)
        verbose_name = _('транзакция')
        verbose_name_plural = _('транзакции')

    def get_wallet(self):
        return self.user.get_ps_account(self.ps)

    def get_abs_amount(self):
        return abs(self.amount)


PLAN_PERIOD_HOUR = 1
PLAN_PERIOD_DAY = 2
PLAN_PERIOD_WEEK = 3
PLAN_PERIOD_MONTH = 4

PLAN_PERIODS = (
    (PLAN_PERIOD_HOUR, _('В час')),
    (PLAN_PERIOD_DAY, _('В сутки')),
    (PLAN_PERIOD_WEEK, _('В неделю')),
    (PLAN_PERIOD_MONTH, _('В месяц')),
)


class PlanManager(models.Manager):
    def get_plan_by_amount(self, amount):
        try:
            return self.get(min_amount__lte=amount, max_amount__gte=amount)
        except:
            return None


class Plan(models.Model):
    title = models.CharField(_('Название'), max_length=50, null=False, blank=False, default='')
    min_amount = models.DecimalField(_('Мин. сумма'), max_digits=8, decimal_places=2, default=1, null=False,
                                     blank=False)
    max_amount = models.DecimalField(_('Макс. сумма'), max_digits=8, decimal_places=2, default=100, null=False,
                                     blank=False)
    percent = models.DecimalField(_('Процент'), max_digits=7, decimal_places=2, default=0, null=False, blank=False)
    period = models.IntegerField(_('Период'), blank=False, null=False, choices=PLAN_PERIODS, default=2)

    objects = PlanManager()

    class Meta:
        ordering = ('min_amount', 'max_amount', 'percent')
        verbose_name = _('инвестиционный план')
        verbose_name_plural = _('инвестиционные планы')

    def __str__(self):
        return self.title



