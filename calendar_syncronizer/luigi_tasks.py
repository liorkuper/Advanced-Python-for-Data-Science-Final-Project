import luigi
from luigi import ExternalTask, Parameter, Task, build, Parameter
import pandas as pd
import ast

from calendars_processing import weekly_schedule_array, calendar_to_array, get_calendar_events, get_busy_timeslots
from placements_logic import potential_classes, chosen_classes
from write_to_calendar import write_to_calendar

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class Get_My_Calendar_Data(Task):
    calendar_id = 'lior69966996@gmail.com'
    path = 'data/My_Calendar_Data.csv'

    def output(self):
        return luigi.LocalTarget(self.path)

    def run(self):
        my_busy_timeframes = get_busy_timeslots(self.calendar_id)[self.calendar_id]['busy']
        my_calendar_mapping = calendar_to_array(my_busy_timeframes)
        with self.output().open('w') as f:
            my_calendar_mapping.to_csv(f)


class Get_Gym_Calendar_Data(Task):
    calendar_id = 'vs1h2duqu6ku7m8vm3kp0ufsl0@group.calendar.google.com'
    path = 'data/Gym_Calendar_Data.csv'

    def output(self):
        return luigi.LocalTarget(self.path)

    def run(self):
        my_busy_timeframes = get_busy_timeslots(self.calendar_id)[self.calendar_id]['busy']
        my_calendar_mapping = calendar_to_array(my_busy_timeframes)
        with self.output().open('w') as f:
            my_calendar_mapping.to_csv(f)


class Process_Data(Task):
    gym_calendar_id = 'vs1h2duqu6ku7m8vm3kp0ufsl0@group.calendar.google.com'
    path_chosen_classes_to_schedule = 'data/chosen_classes_to_schedule.txt'
    path_all_gym_classes = 'data/all_gym_classes.txt'

    def requires(self):
        return {'Get_My_Calendar_Data': self.clone(Get_My_Calendar_Data),
                'Get_Gym_Calendar_Data': self.clone(Get_Gym_Calendar_Data)}

    def output(self):
        return {'chosen_classes_to_schedule' : luigi.LocalTarget(self.path_chosen_classes_to_schedule),
                'all_gym_classes': luigi.LocalTarget(self.path_all_gym_classes)}

    def run(self):
        with open(self.input()['Get_My_Calendar_Data'].path, 'r') as in_file:
            my_calendar_mapping = pd.read_csv(in_file)
        with open(self.input()['Get_Gym_Calendar_Data'].path, 'r') as in_file:
            gym_calendar_mapping = pd.read_csv(in_file)

        potential_classes_matrix = potential_classes(my_calendar=my_calendar_mapping, gym_calendar=gym_calendar_mapping)
        chosen_classes_to_schedule = chosen_classes(potential_classes_matrix, gym_calendar_mapping)
        all_gym_classes = get_calendar_events(self.gym_calendar_id)

        with self.output()['chosen_classes_to_schedule'].open('w') as f:
            f.write(str(chosen_classes_to_schedule))

        with self.output()['all_gym_classes'].open('w') as f:
            f.write(str(all_gym_classes))


class pushing_to_user_calendar(Task):

    def requires(self):
        return self.clone(Process_Data)

    def run(self):
        with open('data/all_gym_classes.txt', 'r') as in_file:
            all_gym_classes = in_file.read()
            all_gym_classes_list=ast.literal_eval(all_gym_classes)

            with open('data/chosen_classes_to_schedule.txt', 'r') as in_file:
                chosen_classes_to_schedule = in_file.read()
                chosen_classes_to_schedule_list=ast.literal_eval(chosen_classes_to_schedule)

                for timestamp in chosen_classes_to_schedule_list:
                    for k in all_gym_classes_list:
                        title = k[0]
                        start_time = k[1]
                        end_time = k[2]
                        if start_time == timestamp:
                            write_to_calendar(title, start_time, end_time, timezone='Asia/Tel_Aviv')


# build([Get_My_Calendar_Data()], local_scheduler=True)
# build([Get_Gym_Calendar_Data()], local_scheduler=True)
# build([Process_Data()], local_scheduler=True)



# Tasks:
# 1. generate my calendar data- DONE
# 2. generate gym calendar data- DONE
# 3. process data- DONE
# 4. push results to google calendar