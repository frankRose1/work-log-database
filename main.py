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
    employee= CharField(max_length=150)
    title = CharField(max_length=200)
    date = DateField()
    notes = TextField()


def initialize_db():
    """Connect to the database and create the tables"""
    db.connect()
    db.create_tables([Task], safe=True)

def add_task():
    """Create a new task entry"""
    employee_name = input('Employee name: ').strip()
    task_title = input('Title: ').strip()
    task_date = get_date_input()
    task_notes = input('Notes: ').strip()
    if input('Save entry? [Yn] ').lower().strip() != 'n':
        Task.create(employee=employee_name, title=task_title, date=task_date, notes=task_notes)
        print('Entry saved!')

def search_tasks():
    """Search tasks"""
    pass

def quit_program():
    """Quit program"""
    print('\nUser has ended the program.')

def get_date_input():
    """Get task date from the user"""
    while True:
        date_str = input('Task date, use DD/MM/YYYY format: ').strip()
        try:
            date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
            break
            return date
        except ValueError:
            print('Error: {} doesn\'t seem to be a valid date, please try again.'.format(date_str))

def delete_task(task):
    """Deletes a task from the Database"""
    if input('Are your sure? [yN] ').lower().strip() == 'y':
        task.delete_instance()
        print('Task was deleted!')


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
