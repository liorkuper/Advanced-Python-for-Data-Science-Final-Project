from __future__ import print_function
import datetime
import random

import pytz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def potential_classes(my_calendar, gym_calendar):
    """
    The function receives 2 calendar mapping DataFrames,
    and returns a DataFrame with all the potential fitness classes (0=no potential class, 1=potential class)

    :input: 2 DataFrames
    :return: pandas DataFrame
    """
    temp_potential_classes_output = gym_calendar.sub(my_calendar)
    potential_classes_output = temp_potential_classes_output.replace(-1, 0)
    return potential_classes_output


def chosen_classes(potential_classes_matrix):
    """
    :input: potential_classes_matrix:
            a DataFrame with all the potential fitness classes (0=no potential class, 1=potential class)
    :returns: a list of chosen fitness class timezones, in the following format:
              [(event_title, start_dateTime, end_dateTime), (event_title, start_dateTime, end_dateTime)...]
    """

    # extracting calendar format dates for matching fitness events
    count = 0
    output_list = []
    # For simplicity, I assumed that there are more than 4 optional
    # timeslots and used a random choosing mechanism
    while count < 4:
        row = random.randint(0, 23)
        column = random.randint(0, 6)
        if potential_classes_matrix.iloc[row, column] == 1:
            count += 1
            tz = pytz.timezone('Asia/Tel_Aviv')
            date = potential_classes_matrix.columns[column]
            output_list.append(tz.localize(datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]), int(row))).isoformat())
    return output_list

