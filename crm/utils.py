"""A unit with description of calendar class"""

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        """Will return an HTML string with list of events for the day"""
        events_per_day = events.filter(date=day)
        result = ""
        for event in events_per_day:
            result += f"<li>{event.type}</li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{result}</ul></td>"
        return "<td></td>"

    def formatweek(self, theweek, events):
        """Will return an HTML string for one week splited with days returned from
         'formday' method"""
        week = ""
        for d_number, weekday in theweek:
            week += self.formatday(d_number, events)
        return f"<tr>{week}</tr>"

    def formatmonth(self, withear=True):
        """Will return a table for one moth using HTMLCalendar basic and formatweek methods"""
        events = Event.objects.filter(date__year=self.year, sate__month=self.moth)
        cal = "<table border='0' collspacing='0' class='calendar'>\n"
        cal += f"{self.formatmothname(self.year, self.month, withear=withear)}\n"
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.motn):
            cal += f"{self.formatweek(week, events)}\n"
        return cal
