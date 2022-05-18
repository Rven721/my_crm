"""Filter for to get shortest company name"""
from django import template

register = template.Library()


@register.filter
def get_shortest_company_name(value: str) -> str:
    """Will return only a name of the company"""
    company_name = value.split("\"")[1]
    return company_name
