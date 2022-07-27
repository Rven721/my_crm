"""a module to connect with google calendar"""
import datetime
import os
import os.path
import base64
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .busines_logic.period_getter import get_next_period


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
CAL_ID = os.environ.get("GC_ID", "d4j0fhuooppbbr02ne8b57qmsg@group.calendar.google.com")
FLOW_REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://localhost:8000/calendar/gc/")


def make_creds_file(gc_creds_hash):
    """Will generate file with credentials for google calendar"""
    creds = base64.b32decode(gc_creds_hash.encode()).decode().split(';', maxsplit=1)[0]
    with open('credentials.json', mode='w', encoding='utf-8') as cred_file:
        cred_file.write(creds)


def add_refresh_token(credentials):
    """Will add a refresh token to the credentials and return a json credentials for"""
    creds = credentials.to_json()
    j_creds = json.loads(creds)
    j_creds['refresh_token'] = "hellyes"
    creds = json.dumps(j_creds)
    return creds


def remove_creds_files():
    """Will remove file with credentials"""
    file_path = os.getcwd()
    creds_file = file_path + '/credentials.json'
    token_file = file_path + '/token.json'
    try:
        os.remove(creds_file)
        os.remove(token_file)
    except FileNotFoundError:
        pass


def get_google_approvment():
    """Will make flow and send request for approvment"""
    if not os.path.exists('credentials.json'):
        try:
            make_creds_file(os.environ.get("GC_CRED_HASH"))
        except AttributeError:
            return None
    flow = Flow.from_client_secrets_file('credentials.json', scopes=SCOPES)
    flow.redirect_uri = FLOW_REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )
    return [authorization_url, state]


def handle_google_response(request):
    """Will handle a google server response and create creds token file"""
    request.session['code'] = request.GET['code']
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        state=request.session['state'],
    )
    flow.redirect_uri = FLOW_REDIRECT_URI
    flow.fetch_token(code=request.session['code'])
    credentials = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': 'yes',
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }
    j_creds = add_refresh_token(credentials)
    with open('token.json', mode='w', encoding='utf-8') as token_file:
        token_file.write(j_creds)


def get_creds():
    """Will return credentials,
    or try to update/create new
    """
    if not os.path.exists('credentials.json'):
        try:
            make_creds_file(os.environ.get("GC_CRED_HASH"))
        except AttributeError:
            return None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        return creds
    return None


def build_service(creds):
    """Will make a service to connect to google_calendar,
    with given token or try to make or update token
    """
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError:
        return None


def get_google_calendar_events(month=None, year=None):
    """will return a list of events for a month"""
    creds = get_creds()
    if creds:
        service = build_service(creds)
    else:
        return None
    if not month and not year:
        now = datetime.datetime.now()
        month = now.month
        year = now.year
    month_begin = datetime.datetime(year, month, 1).isoformat() + 'Z'
    next_period = get_next_period(year, month)
    next_month = datetime.datetime(next_period['year'], next_period['month'], 1).isoformat() + 'Z'
    try:
        events_result = service.events().list(calendarId=CAL_ID,
                                              timeMin=month_begin,
                                              timeMax=next_month,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events
    except HttpError:
        return None


def build_event_summary(event):
    """Will return a name of a company connected to event"""
    event_company = event.projects.first().company
    event_company_short_name = event_company.short_name.split('"')[1]
    return event_company_short_name


def build_calendar_event_body(event):
    """Will crate a body for google calendar event"""
    date = event.date.isoformat()
    time = event.time.isoformat()
    start = datetime.datetime.fromisoformat(f"{date} {time}")
    delta = datetime.timedelta(hours=1)
    end = start + delta
    calendar_event = {
        'summary': build_event_summary(event),
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
    creds = get_creds()
    if creds:
        service = build_service(creds)
    else:
        return None
    event_body = build_calendar_event_body(event)
    cal_event = service.events().insert(calendarId=CAL_ID, body=event_body).execute()
    return cal_event


def update_google_calndar_evnet(event):
    """Will add an event to calendar"""
    creds = get_creds()
    if creds:
        service = build_service(creds)
        event_body = build_calendar_event_body(event)
        service.events().update(calendarId=CAL_ID, eventId=event.gc_event_id, body=event_body).execute()


if __name__ == '__main__':
    get_creds()
