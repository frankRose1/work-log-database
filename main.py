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

class Task(Model):
    employee= CharField(max_length=150)
    title = CharField(max_length=200)
    time_spent = IntegerField()
    date = DateField()
    notes = TextField(null=True)

    class Meta:
        database = db


def initialize_db():
    """Connect to the database and create the tables"""
    db.connect()
    db.create_tables([Task], safe=True)


def view_tasks(tasks):
    """Cycle through any tasks found and allow user to edit/delete a task
    Arguments:
        :tasks: list of tasks found
    """
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

def get_task_data():
    """Gets the task data from the user"""
    employee_name = input('Employee name: ').strip()
    task_title = input('Title: ').strip()
    task_time = get_time_input()
    task_date = get_date_input()
    task_notes = input('Notes (optional): ').strip()
    return {
        'employee': employee_name,
        'title': task_title,
        'time_spent': task_time,
        'date': task_date,
        'notes': task_notes
    }


def add_task():
    """Create a new task entry"""
    new_task = get_task_data()
    if input('Save entry? [Yn] ').lower().strip() != 'n':
        Task.create(employee=new_task['employee'], title=new_task['title'], 
                    time_spent=new_task['time_spent'], date=new_task['date'], notes=new_task['notes'])
        print('Entry added!')

def delete_task(task):
    """Deletes a task from the Database"""
    if input('Are your sure? [yN] ').lower().strip() == 'y':
        task.delete_instance()
        print('Task was deleted!')

def edit_task(task):
    """Updates/saves a task"""
    updated_task = get_task_data()
    if input('Update entry? [Yn] ').lower().strip() != 'n':
        task.employee = updated_task['employee']
        task.title = updated_task['title']
        task.time_spent = updated_task['time_spent']
        task.date = updated_task['date']
        task.notes = updated_task['notes']
        task.save()
        print('Task updated!')

def search_by_name():
    """Search by employee name"""
    name_to_search = input('Employee name: ')
    tasks = Task.select().where(Task.employee.contains(name_to_search)).order_by(Task.date.desc())
    view_tasks(tasks)

def search_by_date():
    """Search by date"""
    pass

def search_by_time():
    """Search by time spent on task"""
    pass

def search_by_term():
    """Search by a term in either title or notes"""
    pass

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


def quit_program():
    """Quit program"""
    print('\nUser has ended the program.')


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
