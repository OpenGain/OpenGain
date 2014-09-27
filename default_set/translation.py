from modeltranslation.translator import translator, TranslationOptions
from default_set.models import Plan


class PlansTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Plan, PlansTranslationOptions)
