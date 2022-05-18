"""Filter for to get shortest company name"""
from django import template

register = template.Library()


@register.filter
def my_thousand_separator(value):
    """Will return a given number splited with thosands and with two symbols aftre dot"""
    after_point = ('%.2f' % value).split('.')[1]
    value = str(int(value))
    result = []
    while len(value) >= 4:
        result.append(str(value[-1:-4:-1])[::-1])
        value = str(int(value) // 1000)
    result.append(value)
    res = f"{' '.join(result[::-1])} руб. {after_point} коп."
    return res
