"""
A set of views for calendar
"""

from datetime import datetime
from django.shortcuts import render
from .utils import MyCalendar


def calendar_view(request):
    """A clendar view"""
    month = datetime.now().month
    year = datetime.now().year
    cal = MyCalendar(year, month)
    ctx = {
        "cal": cal.get_the_month(),
    }
    return render(request, 'cal/calendar.html', ctx)
