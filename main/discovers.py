from django.conf import settings
from django.utils.importlib import import_module


def payment_systems():
    retval = []
    for app in settings.INSTALLED_APPS:
        try:
            module = import_module(app)
            if module.IS_PAYMENT_SYSTEM:
                retval.append(module)
        except:
            continue
    return retval


PAYMENT_SYSTEMS = payment_systems()

PAYMENT_SYSTEMS_TUPLE = tuple([(ps.NAME, ps.TITLE) for ps in PAYMENT_SYSTEMS])