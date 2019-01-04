# Work Log with Database

Command line application that will allow users to enter their name, task worked on, the amount of time, and general notes about the task.
Information will be stored in a Sqlite database and there are various means the search tasks. This is an improvement on a previous project that I did where
tasks were saved to the file system in a csv file. Also includes unit tests.

## App Features

- to start the app, in the command line run `pipenv run python work_log.py`
- Menu loop will prompt users for actions adding tasks, various search methods, and an option to quit the program
- New tasks can be created and added to the database
- Tasks can be searched by date, employee name, time_spent, or term in notes/title
- Can page through search results and options are provided to edit or delete a specific task
- unit tests can be found in tests.py

## Tests

- currently there is 71% coverage
- to run tests:
  - in the root directory run `pipenv run coverage run tests.py`
  - for a detailed report run `pipenv run coverage report -m`

## Technologies Used

- pipenv - to set up a virtual environment
- peewee - as an ORM
- coverage - to see the percentage of code covered by tests
