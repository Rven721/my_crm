"""A logic for event syncronizataion"""
import datetime
from crm.models import Event
from django.core.exceptions import ObjectDoesNotExist


def internal_events_sync(gc_events):
    """wil compare enternal events with GC and update enternal events if nessesary"""
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
