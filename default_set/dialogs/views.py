from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from default_set.dialogs.forms import DialogForm, DialogMessageForm
from default_set.dialogs.models import Dialog, DialogMessage
from default_set.models import UserProfile
from django.db.models.query import Q
from django.utils.translation import ugettext_lazy as _


@login_required
def index(request):
    form = DialogForm(user=request.user, data=request.POST or None)
    dialogs = request.user.dialogs.all()
    if request.method == 'POST' and form.is_valid():
        dialog = request.user.get_dialog_by_user(form.recipient)
        DialogMessage.objects.create(dialog=dialog, user=request.user, message=form.cleaned_data['message'])
        messages.success(request, _('Ваше сообщение отправлено'))
        return redirect('dialogs_index')
    return render(request, 'dialogs/index.html',
                  dict(form=form, dialogs=dialogs)
    )


@login_required
def detail(request, pk):
    form = DialogMessageForm(data=request.POST or None)
    try:
        dialog = Dialog.objects.get(pk=pk)
    except Dialog.DoesNotExist:
        return redirect('dialogs_index')
    if request.user in dialog.users.all():
        dialog_messages = dialog.messages.all().order_by('created')
        dialog_messages.filter(~Q(user=request.user), is_readed=False).update(is_readed=True)
        if request.method == 'POST' and form.is_valid():
            DialogMessage.objects.create(dialog=dialog, user=request.user, message=form.cleaned_data['message'])
            messages.success(request, _('Ваше сообщение отправлено'))
            return redirect('dialogs_detail', pk=pk)
        return render(request, 'dialogs/detail.html',
                      dict(dialog=dialog, dialog_messages=dialog_messages, form=form)
        )
    else:
        return redirect('dialogs_index')