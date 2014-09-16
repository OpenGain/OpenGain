from modeltranslation.translator import translator, TranslationOptions
from default_set.staticpages.models import StaticPage


class StaticPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


translator.register(StaticPage, StaticPageTranslationOptions)
