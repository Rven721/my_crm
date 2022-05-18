"""A filter will cut the frase to givvern number of chars"""

from django import template

register = template.Library()


@register.filter
def cut_string(value: str) -> str:
    """Will return a string cuted to given length and add ... in the end"""
    alowed_length = 30
    if len(value) > alowed_length:
        value = value[0:alowed_length] + '...'
    return value
