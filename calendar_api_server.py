from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from zoneinfo import ZoneInfo

pacific = ZoneInfo("America/Los_Angeles")

# Path to your service account JSON file
SERVICE_ACCOUNT_FILE = 'calendar-dial-63790e1cb8b2.json'

# Initialize Flask app
app = Flask(__name__)

# Set the scopes and authenticate
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Create a service to interact with the Calendar API
service = build('calendar', 'v3', credentials=credentials)

# Set your calendar ID — 'primary' for your main calendar
calendar_id = 'themaskedboiii2@gmail.com'

@app.route("/month_events", methods=["GET"])
def month_events():
    # Set the time window: from now to 30 days in the future
    now = datetime.datetime.now(pacific).isoformat()
    future = (datetime.datetime.now(pacific) + datetime.timedelta(days=30)).isoformat()

    # Fetch events
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        timeMax=future,
        maxResults=1000,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    # Prepare the response
    if not events:
        print("No upcoming events found.")
        return jsonify({"message": "No upcoming events found."})
    
    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_list.append({"start": start, "summary": event['summary']})

    print(f"Found {len(event_list)} events.")
    return jsonify(event_list)

# Run the Flask server on all interfaces (LAN accessible)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)