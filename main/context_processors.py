from django.conf import settings
from default_set.models import Transaction, UserProfile
from django.db.models.query import Q


def settings_prosessor(request):
    return dict(settings=settings)


def protocol_processor(request):
    return dict(protocol='https' if request.is_secure() else 'http')


def statistic_processor(request):
    from datetime import datetime, timedelta
    from django.utils import timezone

    return dict(
        project_start_datetime=settings.PROJECT_START_DATETIME,
        project_work_time=timezone.now() - settings.PROJECT_START_DATETIME,
        registered_users=UserProfile.objects.count(),
        registered_users_in_24h=UserProfile.objects.filter(
            date_joined__gte=datetime.now() - timedelta(hours=24)).count(),
        stat_deposits_count=Transaction.objects.get_deposits().count(),
        stat_deposits_amount=Transaction.objects.get_deposits_amount(),
        stat_withdraws_count=Transaction.objects.get_withdraws().count(),
        stat_withdraws_amount=Transaction.objects.get_withdraws_amount(),
    )

