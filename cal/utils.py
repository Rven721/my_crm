"""
An utilite to create my html calendar with meetings
"""

from calendar import HTMLCalendar
from crm.models import Event


class MyCalendar(HTMLCalendar):
    """A calendar description based on HTMLCalendar"""
    def __init__(self, year=None, month=None):
        self.month = month
        self.year = year
        super().__init__()

    def get_the_day(self, day, events):
        """Will return an HTML string \
           with description of events planed for a day"""
        events = events.filter(date__day=day)
        day_events = ''
        for event in events:
            event_link = f"/events/{event.id}"
            day_events += f"<li><a href={event_link}>{event.time.strftime('%H:%M')}</a></li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{day_events}</ul></td>"
        return "<td></td>"

    def get_the_week(self, week, events):
        """Will return an HTML string of one week"""
        one_week = ""
        for day_of_the_month, day_of_the_week in week:
            one_week += self.get_the_day(day_of_the_month, events)
        return f"<tr>{one_week}</tr>"

    def get_the_month(self):
        """Will return an HTML string to display a month calendar"""
        events = Event.objects.filter(date__year=self.year, date__month=self.month, small=False).order_by('date', 'time')
        cal = "<table border='0' collpadding='0' cellspacing='0' class='calendar'>\n"
        cal += f"{self.formatmonthname(self.year, self.month, withyear=True)}\n"
        cal += f"{self.formatweekheader()}"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.get_the_week(week, events)}\n"
        cal += "</table>"
        return cal
