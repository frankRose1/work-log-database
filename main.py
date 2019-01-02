"""
    Work Log Database

    Terminal application that uses an Sqlite database and allows users to create a task by entering 
    their name, task title, amount of time and any general notes regarding the task. Can also search 
    tasks and view a report in the terminal.
"""
import datetime
import os
from collections import OrderedDict

from database_config import initialize_db, Task

def clear_terminal():
    os.system('clear')
    # os.system('cls' if os.name == 'nt' else 'clear')

def view_tasks(tasks):
    """Cycle through any tasks found and allow user to edit/delete a task
    Arguments:
        :tasks: list of tasks found
    """
    if len(tasks) >= 1:
        results = len(tasks)
        counter = 0
        for task in tasks:
            clear_terminal()
            print('='*20)
            print('Employee: {}'.format(task.employee))
            print('Title: {}'.format(task.title))
            print('Date (YYYY/MM/DD): {}'.format(task.date))
            print('Time Spent (in minutes): {}'.format(task.time_spent))
            if task.notes:
                print('Notes: {}'.format(task.notes))
            print('\nResult {} of {}\n'.format(counter + 1, results))
            print('='*20)
            print('[N]ext, [E]dit, [D]elete [R]eturn to menu')
            next_action = input('Action: [Nedr] ').strip().lower()

            if next_action == 'r':
                break
            elif next_action == 'd':
                delete_task(task)
            elif next_action == 'e':
                edit_task(task)
            counter += 1
    else:
        clear_terminal()
        input('No results found. Press enter to return to search menu ')

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
    name_query = input('Employee name: ')
    tasks = (Task
            .select()
            .where(Task.employee.contains(name_query))
            .order_by(Task.date.desc()))
    view_tasks(tasks)

def search_by_date():
    """Search by date"""
    date_query = get_date_input()
    tasks = (Task
            .select()
            .where(Task.date == date_query)
            .order_by(Task.date.desc()))
    view_tasks(tasks)

def search_by_time():
    """Search by time spent on task"""
    time_query = get_time_input()
    tasks = (Task
            .select()
            .where(Task.time_spent == time_query)
            .order_by(Task.date.desc()))
    view_tasks(tasks)

def search_by_term():
    """Search by a term in either title or notes"""
    term_query = input('Enter your search term: ').strip()
    tasks = (Task
            .select()
            .where(
                (Task.title.contains(term_query)) | 
                (Task.notes.contains(term_query)))
                .order_by(Task.date.desc()))
    view_tasks(tasks)

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
        clear_terminal()
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
        clear_terminal()
        print('WORK LOG DATABASE')
        print('='*17)
        for key, value in main_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        user_choice = input('Your choice: ').lower().strip()
        if user_choice in main_menu:
            main_menu[user_choice]()

if __name__ == '__main__':
    """Initialize the db and print the menu"""
    initialize_db()
    print_main_menu()
