"""a module to connect with google calendar"""
import datetime
import os
import os.path
import base64
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
CAL_ID = os.environ.get("GC_ID", "d4j0fhuooppbbr02ne8b57qmsg@group.calendar.google.com")


def make_creds_file(gc_creds_hash):
    """Will generate file with credentials for google calendar"""
    creds = base64.b32decode(gc_creds_hash.encode()).decode().split(';', maxsplit=1)[0]
    with open('credentials.json', mode='w', encoding='utf-8') as f:
        f.write(creds)


def add_refresh_token(credentials):
    """Will add a refresh token to the credentials and return a json credentials for"""
    creds = credentials.to_json()
    j_creds = json.loads(creds)
    j_creds['refresh_token'] = "hellyes"
    creds = json.dumps(j_creds)
    return creds


def get_creds():
    """Will return credentials,
    or try to update/create new
    """
    creds = None
    if not os.path.exists('credentials.json'):
        try:
            make_creds_file(os.environ.get("GC_CRED_HASH"))
        except AttributeError:
            return None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
            j_creds = add_refresh_token(creds)
        # Save the credentials for the next run
        with open('token.json', 'w', encoding="utf-8") as token:
            token.write(j_creds)
    return creds


def build_service():
    """Will make a service to connect to google_calendar,
    with given token or try to make or update token
    """
    creds = get_creds()
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError:
        return None


def get_google_calendar_events(month=None, year=None):
    """will return a list of events for a month"""
    service = build_service()
    if not month and not year:
        now = datetime.datetime.now()
        month = now.month
        year = now.year
    month_begin = datetime.datetime(year, month, 1).isoformat() + 'Z'
    try:
        events_result = service.events().list(calendarId=CAL_ID, timeMin=month_begin,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events
    except HttpError:
        return None


def build_calendar_event_body(event):
    """Will crate a body for google calendar event"""
    date = event.date.isoformat()
    time = event.time.isoformat()
    start = datetime.datetime.fromisoformat(f"{date} {time}")
    delta = datetime.timedelta(hours=1)
    end = start + delta
    calendar_event = {
        'summary': event.projects.first().name,
        'description': f"/events/{event.id}",
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'Europe/Moscow',
        },
    }
    return calendar_event


def add_google_calendar_event(event):
    """Will add an event to calendar"""
    service = build_service()
    event_body = build_calendar_event_body(event)
    cal_event = service.events().insert(calendarId=CAL_ID, body=event_body).execute()
    return cal_event


def update_google_calndar_evnet(event):
    """Will add an event to calendar"""
    service = build_service()
    event_body = build_calendar_event_body(event)
    service.events().update(calendarId=CAL_ID, eventId=event.gc_event_id, body=event_body).execute()


if __name__ == '__main__':
    get_creds()
