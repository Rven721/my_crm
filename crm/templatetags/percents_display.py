"""Filter for to get shortest company name"""
from django import template

register = template.Library()


@register.filter
def percents_display(value):
    """Will return a given number in percent view"""
    res = str(value * 100).split(".", maxsplit=1)[0] + "%"
    return res
