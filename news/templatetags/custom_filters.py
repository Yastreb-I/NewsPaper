from django import template
from django.template.defaultfilters import stringfilter
from .ProfanityList import profanity_redactor

register = template.Library()  # зарегистрируем наш фильтр


@register.filter
@stringfilter
# Фильтр борьбы с нецензурными словами
def censor(value):
    return profanity_redactor(value)
