"""
An utilite to create my html calendar with meetings
"""
from datetime import datetime
from calendar import HTMLCalendar
from .google_calendar import get_google_calendar_events
from .syncronization import internal_events_sync
from httplib2 import ServerNotFoundError


class MyCalendar(HTMLCalendar):
    """A calendar description based on HTMLCalendar"""
    def __init__(self, year=None, month=None):
        self.month = month
        self.year = year
        super().__init__()

    def get_the_day(self, day, events):
        """
           Will return an HTML string \
           with description of events planed for a day
        """
        day_events = ''
        for event in events:
            try:
                event_date = datetime.fromisoformat(event['start']['dateTime']).date().day
                event_time = datetime.fromisoformat(event['start']['dateTime']).time().strftime("%H:%M")
            except KeyError:
                event_date = datetime.fromisoformat(event['start']['date']).date().day
                event_time = None
            if event_date == day:
                try:
                    event_link = event['description']
                    if 'event' not in event_link:
                        event_link = event['htmlLink']
                except KeyError:
                    event_link = "#"
                day_events += f"\
                    <a href='{event_link}'>\
                      <div class='event'>\
                        {event_time}: {event['summary']}\
                      </div>\
                    </a>\n"
        if day != 0:
            return f"<td><span class='date'>{day}</span>{day_events}</td>"
        return "<td></td>"

    def get_the_week(self, week, events):
        """
           Will return an HTML string of one week \
           using day description got from HTMLCalendar.monthdays2calendar method
        """
        one_week = ""
        for day_description in week:
            day_of_the_month = day_description[0]
            one_week += self.get_the_day(day_of_the_month, events)
        return f"<tr>{one_week}</tr>"

    def get_the_month(self):
        """Will return an HTML string to display a month calendar"""
        try:
            events = get_google_calendar_events(self.month, self.year)
            internal_events_sync(events)
        except (ServerNotFoundError, TypeError):
            return "<h1 class='text-center'>Гугл календарь недоступен<br>\
                         Проверьте подлючение к сети</h1>"
        cal = "<table class='calendar'>\n"
        cal += f"{self.formatmonthname(self.year, self.month, withyear=True)}\n"
        cal += f"{self.formatweekheader()}"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.get_the_week(week, events)}\n"
        cal += "</table>"
        return cal
