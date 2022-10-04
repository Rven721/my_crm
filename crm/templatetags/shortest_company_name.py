"""Filter for to get shortest company name"""
from django import template

register = template.Library()


@register.filter
def get_shortest_company_name(value: str) -> str:
    """Will return only a name of the company"""
    try:
        company_name = value.split("\"")[1]
    except IndexError:
        company_name = value
    return company_name
