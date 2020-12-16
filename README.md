![alt text](https://github.com/csci-e-29/2020fa-final-project-liorkuper/blob/develop/design_Images/upper_bound.png?raw=true)
# Creating Calendars Synchronizer Using Python
### Created by: Lior Kuper
#### 2020FA-CSCI-E29 Advanced Python for Data Science
![alt text](https://github.com/csci-e-29/2020fa-final-project-liorkuper/blob/develop/design_Images/lower_bound.png?raw=true)


* As a person that sees fitness and physical activity of high importance, I often find it difficult to fit it in my weekly
calendar. 
* The different time schedules of the institute where I train is hard to align with the rest
of my responsibilities, and this manual work coordination takes a long time.
* In this project I used Google Calendar's API (for pushing & pulling events) & Luigi workflow to generate a tool aims to automates the process of scheduling the optimal fitness classes to be taken. It does that by using both the user's personal 
and the studio's calendars, and automatically schedules the optimal classes in the user's calendar.

<p align="center"><img width=50% src="https://github.com/csci-e-29/2020fa-final-project-liorkuper/blob/develop/design_Images/google_calendar_api_image.png"></p>


### Implementation overview 
The tool is build of 5 modules:
* ***_tool_runner.py_*** : the tool's entry point. Responsible for initiating the luigi build.
* ***_luigi_tasks.py_*** : includes all the different workflow tasks.
* ***_calendars_processing.py_*** : includes different pre-processing stages for calendars info- pulling calendar events, 
                              transforming a calendar to a pandas DF, extracting 'busy' timeslots etc.
* ***_placements_logic.py_*** : responsible for finding the most suiting fitness classes for the user.
* ***_write_to_calendar.py_*** : responsible for pushing events (=the matching fitness classes) to the user's calendar.


Luigi flow overview:

![alt text](https://github.com/csci-e-29/2020fa-final-project-liorkuper/blob/develop/design_Images/luigi_flow.png?raw=true)


### How can you use my tool?
1. Clone the repo to your desktop
2. In "tool_runner.py", change the input emails to your calendar and your gym's calendar (please read the below note while doing do).
3. CD into local repo & Run in CLI the following commands: 
3. 1. "pipenv install" 
3. 2. "pipenv shell"
3. 3. "python calendar_syncronizer/tool_runner.py"
      At this stage a browser window will be opened and will ask your permission to access your Google Calendar. Approve it.
    
At this point luigi should continue running it's task, until new events are automatically scheduled in your calendar. 

** Importnat note:
   An obstable I encountered while working on this project is that the calendar owner must provide access for the api to clone & write events from his calendar.
   Therefore, unfortunately, I couldn't use my real gym's calendar, so I created a similar calendar for which I had access.
   While running the tool- **make sure you provide 2 calendar you have access to.**
   
 
 ### Future improvements & Reflection
 
 * The "placements logic" could be a lot more sophiticated, and to leverage specific user constraints & ML (for example- by saving data 
   about classes that the user attended or not, and by that to improve the placement mechanisem).
 * This idea can be expanded to any calendars syncrinization scenatio (meeting schedule, doctor apointments etc).
 
 
 ### Additional info
 * Google Calendar API link: https://developers.google.com/calendar
