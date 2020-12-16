from __future__ import print_function
from luigi import build
from luigi_tasks import pushing_to_user_calendar

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    build([pushing_to_user_calendar()], local_scheduler=True)

if __name__ == '__main__':
    main()