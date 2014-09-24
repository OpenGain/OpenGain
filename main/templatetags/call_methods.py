from django import template

register = template.Library()


def callMethod(obj, methodName):
    method = getattr(obj, methodName)

    if obj.__callArg:
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()


def args(obj, arg):
    if not "__callArg" in obj.__dict__:
        obj.__callArg = []

    obj.__callArg += [arg]
    return obj


register.filter("call", callMethod)
register.filter("args", args)