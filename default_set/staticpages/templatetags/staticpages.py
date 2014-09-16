from django import template
from django.conf import settings
from ..models import StaticPage


register = template.Library()


class StaticpageNode(template.Node):
    def __init__(self, context_name, starts_with=None, user=None):
        self.context_name = context_name
        if starts_with:
            self.starts_with = template.Variable(starts_with)
        else:
            self.starts_with = None
        if user:
            self.user = template.Variable(user)
        else:
            self.user = None

    def render(self, context):
        staticpages = StaticPage.objects.all()
        if self.starts_with:
            staticpages = staticpages.filter(
                url__startswith=self.starts_with.resolve(context))

        if self.user:
            user = self.user.resolve(context)
            if not user.is_authenticated():
                staticpages = staticpages.filter()
        else:
            staticpages = staticpages.filter()

        context[self.context_name] = staticpages
        return ''


@register.tag
def get_staticpages(parser, token):
    bits = token.split_contents()
    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "['url_starts_with'] [for user] as context_name" %
                      dict(tag_name=bits[0]))
    if len(bits) >= 3 and len(bits) <= 6:

        if len(bits) % 2 == 0:
            prefix = bits[1]
        else:
            prefix = None

        if bits[-2] != 'as':
            raise template.TemplateSyntaxError(syntax_message)
        context_name = bits[-1]

        if len(bits) >= 5:
            if bits[-4] != 'for':
                raise template.TemplateSyntaxError(syntax_message)
            user = bits[-3]
        else:
            user = None

        return StaticpageNode(context_name, starts_with=prefix, user=user)
    else:
        raise template.TemplateSyntaxError(syntax_message)
