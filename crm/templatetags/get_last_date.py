"""Filter to get date of last event"""
from django import template

register = template.Library()


@register.filter
def get_last_event_date(event_set):
    """will return a las date of event for project"""
    return event_set.order_by('date').last().date
