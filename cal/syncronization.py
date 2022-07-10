"""A logic for event syncronizataion"""
import datetime
import cal.google_calendar as gc
from crm.models import Event
from django.core.exceptions import ObjectDoesNotExist


def internal_events_sync(gc_events):
    """will compare enternal events with GC and update enternal events if nessesary"""
    for gc_event in gc_events:
        try:
            internal_event = Event.objects.get(gc_event_id=gc_event['id'])
            gc_event_data = datetime.datetime.fromisoformat(gc_event['start']['dateTime'])
            if internal_event.date != gc_event_data.date() or \
               internal_event.time != gc_event_data.time():
                internal_event.date = gc_event_data.date()
                internal_event.time = gc_event_data.time()
                internal_event.save()
        except (ObjectDoesNotExist, KeyError):
            next


def external_events_sync():
    """Will add evetns to google calendar if event were added to crm while connections with calendar were loose"""
    no_return_point = datetime.date(2022, 7, 1)
    events = Event.objects.filter(small=True, date__gte=no_return_point, gc_event_id="")
    for event in events:
        gc_event = gc.add_google_calendar_event(event)
        event.gc_event_id = gc_event['id']
        event.save()
