"""Filter to get timedelta of event date and cureent date"""
from django import template
import datetime

register = template.Library()


@register.filter
def check_timespread(event_date: datetime.date) -> bool:
    cur_date = datetime.date.today()
    delta = cur_date - event_date
    if delta.days >= 7:
        return True
    return False
