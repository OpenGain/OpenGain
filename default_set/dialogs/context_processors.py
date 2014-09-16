from django.db.models.query import Q
from default_set.dialogs.models import DialogMessage


def unread_dialogs_messages(request):
    count = 0
    if request.user.is_authenticated():
        dialogs = request.user.dialogs.select_related().filter(users=request.user)
        count = DialogMessage.objects.filter(~Q(user=request.user), dialog__in=dialogs, is_readed=False).count()
    return dict(unread_dialogs_messages=count)

