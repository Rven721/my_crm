"""A filter for returning a shortest company name"""
from django import template

register = template.Library()


@register.filter
def get_shortest_company_name(value: str) -> str:
    """Will return a name of comapny in scobkis"""
    company_name = value.split("\"")[0]
    return company_name
