from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_free_times(date):
    service = get_calendar_service()

    start = datetime.datetime.combine(date, datetime.time.min).isoformat() + 'Z'
    end = datetime.datetime.combine(date, datetime.time.max).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    booked_times = []
    for event in events:
        start_time = event['start'].get('dateTime')
        end_time = event['end'].get('dateTime')
        booked_times.append((start_time, end_time))

    # Generate list of available 1-hour slots between 09:00 and 18:00
    free_times = []
    current_time = datetime.datetime.combine(date, datetime.time(9, 0))
    end_of_day = datetime.datetime.combine(date, datetime.time(18, 0))

    while current_time < end_of_day:
        slot_end = current_time + datetime.timedelta(hours=1)
        if not any(start <= current_time.isoformat() < end for start, end in booked_times):
            free_times.append({
                'start': current_time.isoformat(),
                'end': slot_end.isoformat()
            })
        current_time = slot_end

    return free_times

def add_event_to_google_calendar(appointment):
    service = get_calendar_service()

    event = {
        'summary': f'Appointment with {appointment.name}',
        'start': {'dateTime': appointment.start_time.isoformat(), 'timeZone': 'Europe/Tirane'},
        'end': {'dateTime': (appointment.start_time + datetime.timedelta(hours=1)).isoformat(), 'timeZone': 'Europe/Tirane'},
        'description': appointment.service.name,
    }

    service.events().insert(calendarId='primary', body=event).execute()
