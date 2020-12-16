from __future__ import print_function
from luigi import build
from luigi_tasks import Get_My_Calendar_Data, Get_Gym_Calendar_Data, Process_Data, pushing_to_user_calendar

def main():
    build([pushing_to_user_calendar(user_calendar_id='lior69966996@gmail.com',
                                    gym_calendar_id = 'vs1h2duqu6ku7m8vm3kp0ufsl0@group.calendar.google.com')], local_scheduler=True)

if __name__ == '__main__':
    main()