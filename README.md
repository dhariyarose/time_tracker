# time_tracker
Breif Note:

A multi-user and multi-project work time tracking
application using Django and Django Rest Framework.

Users must login with their email and password.
We have a list of users and projects.
We can add tasks for each project and assign a user to each task(By default status is to_do).
Users can see assigned tasks for each project.
When they are working on a task they should change the status (in progress, done)
Users should be added to the logs( start times and end times).
A user can view the users involved in a project. Their logs can also be viewed.
There is an option to view monthly logs. Monthly logs include total working hours. How many
hours worked by all users on each date. What project and task they worked on on each date.


How to run:
git clone https://github.com/dhariyarose/time_tracker.git
cd time_tracker
virtualenv env_name
source env_name/bin/activate
pip install -r requirements
python3 manage.py makemigrations
python3 manage.py migrate
python manage.py runserver