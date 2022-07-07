"""
A set of views for calendar
"""

from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .utils import MyCalendar
from .busines_logic import period_getter
from .google_calendar import get_google_approvment, handle_google_response, remove_creds_files


@login_required
def get_approvment_view(request):
    """Will send a request to google to get approvment to work with calendar"""
    approvment_data = get_google_approvment()
    if not approvment_data:
        return redirect(reverse('calendar'))
    authorization_url, state = approvment_data
    request.session['state'] = state
    return redirect(authorization_url)


@login_required
def handle_approvment_response_view(request):
    """Handle response"""
    handle_google_response(request)
    return redirect(reverse('calendar'))


@login_required
def clear_credentials_view(request):
    """Will clear session creds and remove credentiasl and token"""
    remove_creds_files()
    try:
        del request.session['credentials']
    except KeyError:
        pass
    return redirect(reverse('calendar'))


@login_required
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


@login_required
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
