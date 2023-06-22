from django import template
from django.template.defaultfilters import stringfilter
from .ProfanityList import profanity_redactor

register = template.Library()  # зарегистрируем наш фильтр


# Фильтр борьбы с нецензурными словами
@register.filter
@stringfilter
def censor(value):
    return profanity_redactor(value)

