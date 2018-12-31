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
    time_spent = IntegerField()
    date = DateField()
    notes = TextField(null=True)


def initialize_db():
    """Connect to the database and create the tables"""
    db.connect()
    db.create_tables([Task], safe=True)


def search_tasks():
    """Search tasks"""
    tasks = Task.select()
    for task in tasks:
        print('='*20)
        print(task.title)
        print(task.employee)
        print(task.date)
        if task.notes:
            print(task.notes)
        print('\n'+'='*20)
        print('[N]ext, [E]dit, [D]elete [R]eturn to menu')
        next_action = input('Action: [Nedr] ').strip().lower()

        if next_action == 'r':
            break
        elif next_action == 'd':
            delete_task(task)
        elif next_action == 'e':
            edit_task(task)

def add_task():
    """Create a new task entry"""
    employee_name = input('Employee name: ').strip()
    task_title = input('Title: ').strip()
    task_time = get_time_input()
    task_date = get_date_input()
    task_notes = input('Notes (optional): ').strip()
    if input('Save entry? [Yn] ').lower().strip() != 'n':
        Task.create(employee=employee_name, title=task_title, 
                    time_spent=task_time, date=task_date, notes=task_notes)
        print('Entry saved!')

def get_date_input():
    """Get task date from the user"""
    while True:
        date_str = input('Task date, use DD/MM/YYYY format: ').strip()
        try:
            date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
            return date
        except ValueError:
            print('Error: {} doesn\'t seem to be a valid date, please try again.'.format(date_str))

def get_time_input():
    """Gets the time spent on the task from the user"""
    while True:
        time_input = input('Time spent on task (in minutes): ')
        try:
            time_input = int(time_input) 
            return time_input
        except ValueError:
            print('Error: "{}" doesn\'t seem to be a valid time. Numbers only!'.format(time_input))

def delete_task(task):
    """Deletes a task from the Database"""
    if input('Are your sure? [yN] ').lower().strip() == 'y':
        task.delete_instance()
        print('Task was deleted!')

def edit_task(task):
    """Updates/saves a task"""
    print(task)

def quit_program():
    """Quit program"""
    print('\nUser has ended the program.')

def search_by_name():
    """Search by employee name"""
    pass

def search_by_date():
    """Search by date"""
    pass

def search_by_time():
    """Search by time spent on task"""
    pass

def search_by_term():
    """Search by a term in either title or notes"""
    pass

search_menu = OrderedDict([
    ('a', search_by_name),
    ('b', search_by_date),
    ('c', search_by_time),
    ('d', search_by_term)
])

def print_search_menu():
    """Search tasks"""
    search_choice = None
    while search_choice != 'q':
        print('Enter "q" to return to main menu')
        for key, value in search_menu.items():
            print('{}) {}'.format(key, value.__doc__))

        search_choice = input('Your choice: ').lower().strip()
        if search_choice in search_menu:
            search_menu[search_choice]()

main_menu = OrderedDict([
    ('a', add_task),
    ('s', print_search_menu),
    ('q', quit_program)
])

def print_main_menu():
    """Print a menu of options for the user"""
    user_choice = None
    while user_choice != 'q':
        for key, value in main_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        user_choice = input('Your choice: ').lower().strip()
        if user_choice in main_menu:
            main_menu[user_choice]()

if __name__ == '__main__':
    """Initialize the db and print the menu"""
    initialize_db()
    print_main_menu()
