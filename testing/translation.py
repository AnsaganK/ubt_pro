from modeltranslation.translator import register, TranslationOptions
from .models import News, Lesson, Pages, Role

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(Pages)
class PagesTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(Role)
class RoleTranslationOptions(TranslationOptions):
    fields = ('name',)