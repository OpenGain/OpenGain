from modeltranslation.translator import translator, TranslationOptions
from default_set.news.models import News


class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)


translator.register(News, NewsTranslationOptions)
