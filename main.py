"""
    Work Log Database

    Terminal application that uses an Sqlite database and allows users to create a task by entering 
    their name, task title, amount of time and any general notes regarding the task. Can also search 
    tasks and view a report in the terminal.
"""
import datetime
from collections import OrderedDict

from peewee import *

db = SqliteDatabase('worklog.db')

class BaseClass(Model):
    class Meta:
        database = db

class Task(BaseClass):
    employee_name = CharField(max_length=80)
    title = CharField(max_length=150)
    date = DateField()
    notes = TextField()


def initialize_db():
    """Connect to the database and create the tables"""
    db.connect()
    db.create_tables([Task], safe=True)

def add_task():
    """Create a new task entry"""
    pass

def search_tasks():
    """Search tasks"""
    pass

def quit_program():
    """Quit program"""
    print('\nUser has ended the program.')

menu = OrderedDict([
    ('a', add_task),
    ('s', search_tasks),
    ('q', quit_program)
])

def print_menu():
    """Print a menu of options for the user"""
    user_choice = None
    while user_choice != 'q':
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        user_choice = input('Your choice: ').lower().strip()
        if user_choice in menu:
            menu[user_choice]()

if __name__ == '__main__':
    """Initialize the db and print the menu"""
    initialize_db()
    print_menu()
