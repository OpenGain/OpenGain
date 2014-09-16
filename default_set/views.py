from importlib import import_module
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from default_set.forms import *
from default_set.models import *
from default_set.transactions import UserTransaction, InsufficientBalance, \
    calculate_withdraw_amount
from default_set.forms import RegistrationForm, WithdrawForm, UserSettingsForm
from django.contrib import messages
from main.discovers import PAYMENT_SYSTEMS, PAYMENT_SYSTEMS_TUPLE
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.utils import translation


@login_required
def index(request):
    return render(request, 'default_set/index.html')


def signin(request):
    form = SignInForm(data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        current_lang = translation.get_language()
        login(request, form.user_cache)
        translation.activate(current_lang)
        form.user_cache.save()
        return redirect(request.GET.get('next', 'account_index'))

    return render(request, 'default_set/signin.html',
                  dict(form=form))


def signup(request):
    form = RegistrationForm(data=request.POST or None,
                            initial=dict(
                                sponsor_username=request.session.get('sponsor',
                                                                     UserProfile.objects.get_main_admin().username)
                            )
    )
    current_lang = translation.get_language()
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        user.lang = current_lang
        user.sponsor = UserProfile.objects.get(
            username=form.cleaned_data.get('sponsor_username', UserProfile.objects.get_main_admin().username))
        user.save()

        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])

        login(request, user)
        translation.activate(current_lang)

        user.email_user(_('Регистрация в проекте {}').format(settings.PROJECT_TITLE), 'mail/registration.html', )

        if user.sponsor.is_alerts_referrals:
            user.sponsor.email_user(_('Новый реферал в проекте {}').format(settings.PROJECT_TITLE),
                                    'mail/new_referral.html', dict(referral=user))
        return redirect('account_index')

    return render(request, 'default_set/signup.html',
                  dict(form=form))


@login_required
def signout(request):
    logout(request)
    return redirect('index')


@login_required
def deposit(request):
    form = DepositForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():

        pending_deposits = request.user.transactions.filter(transaction_type=TRANSACTION_DEPOSIT, is_ended=False)
        if pending_deposits.count() >= 3:
            form.add_error(None, _(
                'У вас имеются 3 или более незавершенные операции пополнения. Пожалуйста, завершите или отмените их на странице "История операций"'))
            return render(request, 'default_set/deposit.html', dict(form=form))

        ps_name = form.cleaned_data.get('ps')
        user_balance = request.user.get_ps_balance(ps_name)

        transaction = request.user.transactions.create(transaction_type=TRANSACTION_DEPOSIT,
                                                       amount=form.cleaned_data.get('amount', 0),
                                                       balance_before=user_balance,
                                                       balance_after=user_balance,
                                                       ps=ps_name)

        return redirect('deposit_continue', pk=transaction.pk)
    return render(request, 'default_set/deposit.html', dict(form=form))


@login_required
def deposit_continue(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, transaction_type=TRANSACTION_DEPOSIT, is_ended=False,
                                    user=request.user)
    module = import_module('payment_systems.' + transaction.ps + '.views')
    continue_view = getattr(module, 'deposit_continue')
    return continue_view(request, transaction, dict(transaction=transaction))


@login_required
def deposit_cancel(request, pk):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, pk=pk, transaction_type=TRANSACTION_DEPOSIT, is_ended=False,
                                        user=request.user)
        transaction.delete()
    return redirect('account_deposit')


@login_required
def withdraw(request):
    form = WithdrawForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ps = form.cleaned_data.get('ps')

        if not request.user.get_ps_account(ps):
            form.add_error('ps', _('Укажите аккаунт платежной системы в настройках'))
        else:
            try:
                amount = form.cleaned_data.get('amount')
                tr = UserTransaction()
                tr.do_transaction_withdraw(
                    user=request.user,
                    ps=ps,
                    amount=amount
                )
                if request.user.is_alerts_other:
                    request.user.email_user(_('Запрос на вывод'), 'mail/withdraw_request.html', dict(
                        ps=tr.transaction.get_ps_display(), amount=amount, balance=tr.balance_after,
                        comission=settings.WITHDRAW_COMISSION_PERCENT,
                        for_withdraw=calculate_withdraw_amount(amount)
                    ))
                messages.success(request, _('Запрос на вывод отправлен'))
                return redirect('account_withdraw')
            except InsufficientBalance:
                form.add_error('amount', _('Недостаточно средств'))

    return render(request, 'default_set/withdraw.html',
                  dict(form=form),
    )


@login_required
def transfer(request):
    form = TransferForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        if form.cleaned_data.get('username') == request.user.username:
            form.add_error('username', _('Вы не можете сделать перевод самому себе'))
        else:
            try:
                tr = UserTransaction().do_transaction_transfer(
                    user=request.user,
                    ps=form.cleaned_data.get('ps'),
                    amount=form.cleaned_data.get('amount'),
                    other_user=UserProfile.objects.get(username=form.cleaned_data.get('username'))
                )
                messages.success(request, _('Внутренний перевод успешно отправлен'))
                return redirect('account_transfer')
            except InsufficientBalance:
                form.add_error('amount', _('Недостаточно средств'))
    return render(request, 'default_set/transfer.html',
                  dict(form=form), )


@login_required
def referrals(request):
    return render(request, 'default_set/referrals.html')


@login_required
def history(request):
    transaction_type = request.GET.get('type', None)

    ALLOWED_TRANSACTIONS = [
        'TRANSACTION_DEPOSIT', 'TRANSACTION_WITHDRAW', 'TRANSACTION_TRANSFER_OUTGOING',
        'TRANSACTION_TRANSFER_INCOMING', 'TRANSACTION_REFERRAL', 'TRANSACTION_ACCRUAL'
    ]

    if transaction_type and transaction_type not in ALLOWED_TRANSACTIONS:
        raise Http404

    if transaction_type:
        module = import_module('default_set.models')
        if hasattr(module, str(transaction_type)) and getattr(module, str(transaction_type)).__class__ == int:
            transactions = request.user.transactions.filter(
                transaction_type=getattr(module, str(transaction_type))
            )
        else:
            transactions = request.user.transactions.all()
    else:
        transactions = request.user.transactions.all()

    return render(request, 'default_set/history.html',
                  dict(transactions=transactions.order_by('-created'))
    )


@login_required
def profile_settings(request):
    if request.method == 'POST':
        if 'password-old_password' in request.POST:
            pass_form = PasswordChangeForm(data=request.POST, user=request.user, prefix='password')
            if pass_form.is_valid():
                pass_form.save()
                messages.success(request, _('Пароль успешно изменен'))
                return redirect('account_settings')
        else:
            pass_form = PasswordChangeForm(user=request.user, prefix='password')

        if 'settings-timezone' in request.POST:
            form = UserSettingsForm(data=request.POST, instance=request.user, prefix='settings')
            if form.is_valid():
                form.save()
                messages.success(request, _('Данные профиля успешно обновлены'))
                return redirect('account_settings')
        else:
            form = UserSettingsForm(instance=request.user, prefix='settings')

    else:
        form = UserSettingsForm(instance=request.user, prefix='settings')
        pass_form = PasswordChangeForm(user=request.user, prefix='password')

    return render(request, 'default_set/settings.html',
                  dict(form=form, pass_form=pass_form)
    )


@login_required
def payment_systems_settings(request):
    forms = []

    for ps in PAYMENT_SYSTEMS:
        module = import_module('payment_systems.' + ps.NAME + '.forms')
        form_class = getattr(module, 'PSForUserForm')

        instance = None
        try:
            instance = getattr(request.user, ps.NAME)
        except ObjectDoesNotExist:
            module = import_module('payment_systems.' + ps.NAME + '.models')
            getattr(module, 'PSForUser').objects.create(user=request.user)

        if request.method == 'POST' and ps.NAME + '-wallet' in request.POST:
            temp_form = form_class(data=request.POST, instance=instance or getattr(request.user, ps.NAME),
                                   prefix=ps.NAME)
            if temp_form.is_valid():
                temp_form.save()
                messages.success(request, _('Платежный аккаунт успешно сохранен'))
                return redirect('account_payment_systems_settings')
            forms.append(temp_form)
        else:
            forms.append(form_class(instance=instance or getattr(request.user, ps.NAME), prefix=ps.NAME))

    return render(request, 'default_set/payment_systems_settings.html',
                  dict(forms=forms)
    )


def sponsor_redirect(request, b64):
    try:
        user = UserProfile.objects.get_user_by_b64username(b64)
        request.session['sponsor'] = user.username
    except UserProfile.DoesNotExist:
        pass
    return redirect(settings.REFLINK_REDIRECT)
