from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def write_to_calendar(event_title, start_dateTime, end_dateTime, timezone='Asia/Tel_Aviv'):
    """
    Function input:
        1. event_title: the name of the event, as it will appear in the user's calendar.
        2. start_dateTime: date and time of event start. Format example: '2020-12-20T09:00:00-07:00'
        3. end_dateTime: date and time of event end. Format example: '2020-12-20T09:00:00-07:00'
        4. timezone: user calendar timezone.
    using these parameters, it creates a new event in the user's Google Calendar
    """

    # Taking care of api credentials
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../token.pickle'):
        with open('../token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the calendar API & write event
    event = {
        'summary': event_title,
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': start_dateTime,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_dateTime,
            'timeZone': timezone,
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))