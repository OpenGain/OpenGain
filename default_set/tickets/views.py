from django.shortcuts import render, redirect
from default_set.tickets.forms import *
from django.contrib.auth.decorators import login_required
from default_set.tickets.models import *
from django.contrib import messages
from django.db.models.query import Q
from django.utils.translation import ugettext_lazy as _


@login_required
def index(request):
    if request.user.is_superuser:
        ticket_list = Ticket.objects.all().order_by('-created')
    else:
        ticket_list = Ticket.objects.filter(user=request.user).order_by('-created')
    return render(request, 'tickets/index.html',
                  dict(ticket_list=ticket_list),
    )


@login_required
def create(request):
    form = TicketForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ticket = Ticket.objects.create(user=request.user, subject=form.cleaned_data['subject'])
        TicketMessage.objects.create(ticket=ticket, message=form.cleaned_data['text'], user=request.user)
        messages.success(request, _('Создан новый тикет'))
        return redirect('tickets_index')
    return render(request, 'tickets/new.html',
                  dict(form=form)
    )


@login_required
def detail(request, pk):
    form = TicketMessageForm(data=request.POST or None)
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return redirect('tickets_index')
    if request.user == ticket.user or request.user.is_superuser:
        ticket_messages = ticket.messages.all().order_by('created')
        ticket_messages.filter(~Q(user=request.user), is_readed=False).update(is_readed=True)
        if request.method == 'POST' and form.is_valid():
            TicketMessage.objects.create(ticket=ticket, message=form.cleaned_data['message'], user=request.user)
            messages.success(request, _('Создано новое сообщение'))
            return redirect('tickets_detail', pk=pk)
        return render(request, 'tickets/detail.html',
                      dict(ticket=ticket, ticket_messages=ticket_messages, form=form)
        )
    else:
        return redirect('tickets_index')


@login_required
def close(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return redirect('tickets_index')
    if ticket.user == request.user or request.user.is_superuser:
        ticket.is_closed = True
        ticket.save()
        messages.success(request, _('Тикет закрыт'))
        return redirect('tickets_index')
    else:
        return redirect('tickets_index')
