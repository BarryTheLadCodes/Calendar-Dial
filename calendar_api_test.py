from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from zoneinfo import ZoneInfo

pacific = ZoneInfo("America/Los_Angeles")

# Path to your service account JSON file
SERVICE_ACCOUNT_FILE = 'calendar-dial-63790e1cb8b2.json'

# Set the scopes and authenticate
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Create a service to interact with the Calendar API
service = build('calendar', 'v3', credentials=credentials)

# Set your calendar ID — 'primary' for your main calendar
calendar_id = 'themaskedboiii2@gmail.com'

# Set the time window: now to some future date
now = datetime.datetime.now(pacific).isoformat()
future = (datetime.datetime.now(pacific) + datetime.timedelta(days=30)).isoformat()

# Fetch events
events_result = service.events().list(
    calendarId=calendar_id,
    timeMin=now,
    timeMax=future,
    maxResults=100,
    singleEvents=True,
    orderBy='startTime'
).execute()

events = events_result.get('items', [])

# Print the events
if not events:
    print("No upcoming events found.")
else:
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start} — {event['summary']}")
