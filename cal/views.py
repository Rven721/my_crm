"""
A set of views for calendar
"""

from datetime import datetime
from django.shortcuts import render
from .utils import MyCalendar
from .busines_logic import period_getter


def calendar_view(request):
    """A clendar view"""
    month = datetime.now().month
    year = datetime.now().year
    cal = MyCalendar(year, month)
    next_period = period_getter.get_next_period(year, month)
    prev_period = period_getter.get_prev_period(year, month)
    ctx = {
        "cal": cal.get_the_month(),
        "next_month": next_period['month'],
        "next_year": next_period['year'],
        "prev_month": prev_period['month'],
        "prev_year": prev_period['year'],
    }
    return render(request, 'cal/calendar.html', ctx)


def given_month_calendar_view(request, year, month):
    """Render a calendar for given month"""
    cal = MyCalendar(year, month)
    next_period = period_getter.get_next_period(year, month)
    prev_period = period_getter.get_prev_period(year, month)
    ctx = {
        "cal": cal.get_the_month(),
        "next_month": next_period['month'],
        "next_year": next_period['year'],
        "prev_month": prev_period['month'],
        "prev_year": prev_period['year'],
    }
    return render(request, 'cal/calendar.html', ctx)
