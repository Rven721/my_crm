"""
A set of views for calendar
"""

from datetime import datetime
from django.shortcuts import render
from crm.models import Task
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


def user_calendar_view(request, user_id):
    """Render a calencar with tasks of the user"""
    month = datetime.now().month
    year = datetime.now().year
    cal = MyCalendar(year, month)
    tasks = Task.objects.filter(doer__id=user_id)
    ctx = {
        "cal": cal.get_the_month(tasks),
    }
    return render(request, 'cal/calendar.html', ctx)
