from __future__ import print_function
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz

import datetime
import pandas as pd
import numpy as np

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def weekly_schedule_array():
    """
    The function creates a base array of a weekly schedule (columns = 7 days x rows = 24 hours)
    :return: pandas DataFrame
    """
    column_names = [datetime.date.today() + datetime.timedelta(days=x) for x in range(7)]
    column_names_str = [str(item) for item in column_names]
    row_names = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
    zeros_array = np.zeros((24, 7))
    output = pd.DataFrame(data=zeros_array, columns=column_names_str, index=row_names)
    return output


def calendar_to_array(busy_timeframes_list):
    """
    The function receives the user's busy timeframes
    and returns a pandas DataFrame with a mapping of all the user's busy times (0=free, 1=busy)

    :input: list of dictionaries
    :return: pandas DataFrame
    """

    # Creating a weekly schedule array (7 days x 24 hours) with zeros
    calc_df = weekly_schedule_array()

    for i in range(len(busy_timeframes_list)):
        event_length = int(busy_timeframes_list[i]['end'][11:13]) - int(busy_timeframes_list[i]['start'][11:13])

        # filling all the hours in which the user is busy
        for hour in range(event_length):
            row_index = int(busy_timeframes_list[i]['start'][11:13]) + hour
            column_index = busy_timeframes_list[i]['start'][0:10]
            calc_df.iloc[row_index, calc_df.columns.get_loc(column_index)] = 1
    return calc_df


def get_calendar_events(calendar_ID='primary'):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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


    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    tz = pytz.timezone('Asia/Tel_Aviv')
    the_datetime = tz.localize(datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)).isoformat()
    the_datetime2 = tz.localize((datetime.datetime.today()+datetime.timedelta(days=6)).replace(hour=23, minute=0, second=0, microsecond=0)).isoformat()
    events_result = service.events().list(calendarId=calendar_ID,
                                          timeMin=the_datetime,
                                          timeMax=the_datetime2,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    output_list=[]

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        title = event['summary']
        output_list.append((title, start, end))
    return output_list

def get_busy_timeslots(calendar_ID='primary'):
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

    # Call the Calendar API
    service = build('calendar', 'v3', credentials=creds)

    # Extract busy times calendar for next 7 days
    tz = pytz.timezone('Asia/Tel_Aviv')
    the_datetime = tz.localize(datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
    the_datetime2 = tz.localize((datetime.datetime.today()+datetime.timedelta(days=6)).replace(hour=23, minute=0, second=0, microsecond=0))
    body = {
      "timeMin": the_datetime.isoformat(),
      "timeMax": the_datetime2.isoformat(),
      "timeZone": 'Asia/Tel_Aviv',
      "items": [{"id": calendar_ID}]
    }

    eventsResult = service.freebusy().query(body=body).execute()
    my_calendar_dict = eventsResult[u'calendars']
    return my_calendar_dict
