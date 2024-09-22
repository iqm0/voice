import datetime
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_events():
    """Fetches upcoming events from Google Calendar."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=51205, redirect_uri_trailing_slash=False)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    time_max = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(weeks=4)).isoformat()
    print(f"Fetching events between {now} and {time_max}")

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=time_max,
        singleEvents=True,
        orderBy='updated').execute()

    events = events_result.get('items', [])
    return events

def classify_reservation(event_summary):
    """Basic classification based on keywords."""
    summary = event_summary.lower()
    if "restaurant" in summary or "dinner" in summary or "lunch" in summary:
        return "Restaurant"
    elif "movie" in summary or "cinema" in summary or "film" in summary:
        return "Movie"
    elif "flight" in summary or "airport" in summary:
        return "Flight"
    else:
        return "Unknown"

def extract_possible_business_name(summary):
    """Extracts possible business name from summary."""
    import re
    match = re.search(r'(?:restaurant booking:|dinner\s+at|DINNER\s+AT|lunch\s+at|LUNCH\s+AT|meeting\s+at|event\s+at|at|:)\s*(.+)', summary, re.IGNORECASE)
    if match:
        name = match.group(1).strip()
        name = re.sub(r'^(LUNCH|DINNER|MEETING)\s+at\s+', '', name, flags=re.IGNORECASE)
        return name
    return ""